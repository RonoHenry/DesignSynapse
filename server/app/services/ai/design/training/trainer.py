"""Training script for the Design Generator model."""

import torch
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from pathlib import Path
import logging
from tqdm import tqdm
from typing import Dict, Any, Tuple

from app.services.ai.design.model import DesignGeneratorModel
from app.services.ai.design.data.loader import create_data_loaders
from app.services.ai.design.training.losses import DesignLoss
from app.services.ai.design.config.training_config import TrainingConfig

class Trainer:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.device = torch.device(config.device)
        
        # Initialize model
        self.model = DesignGeneratorModel(vars(config))
        self.model.to(self.device)
        
        # Initialize optimizer
        self.optimizer = AdamW(
            self.model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay
        )
        
        # Initialize scheduler
        self.scheduler = CosineAnnealingLR(
            self.optimizer,
            T_max=config.num_epochs
        )
        
        # Initialize loss function
        self.criterion = DesignLoss(vars(config))
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Initialize metrics
        self.best_val_loss = float('inf')
        self.patience_counter = 0
        
    def train(self, data_dir: Path):
        """Train the model."""
        # Create data loaders
        train_loader, val_loader = create_data_loaders(
            data_dir=data_dir,
            batch_size=self.config.batch_size,
            num_workers=self.config.num_workers,
            validation_split=self.config.validation_split
        )
        
        # Training loop
        for epoch in range(self.config.num_epochs):
            self.logger.info(f"Epoch {epoch+1}/{self.config.num_epochs}")
            
            # Training phase
            train_metrics = self._train_epoch(train_loader)
            self.logger.info(f"Training metrics: {train_metrics}")
            
            # Validation phase
            val_metrics = self._validate(val_loader)
            self.logger.info(f"Validation metrics: {val_metrics}")
            
            # Learning rate scheduling
            self.scheduler.step()
            
            # Save checkpoint
            if (epoch + 1) % self.config.save_every_n_epochs == 0:
                self._save_checkpoint(epoch, val_metrics)
            
            # Early stopping
            if self._check_early_stopping(val_metrics["total_loss"]):
                self.logger.info("Early stopping triggered")
                break
    
    def _train_epoch(self, train_loader) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train()
        metrics = {
            "total_loss": 0.0,
            "floor_plan_loss": 0.0,
            "elevation_loss": 0.0,
            "specs_loss": 0.0
        }
        
        for batch_idx, (inputs, targets) in enumerate(tqdm(train_loader)):
            # Move data to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            targets = {k: v.to(self.device) for k, v in targets.items()}
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(inputs["features"])
            
            # Calculate loss
            losses = self.criterion(outputs, targets)
            total_loss = losses["total_loss"]
            
            # Backward pass
            total_loss.backward()
            torch.nn.utils.clip_grad_norm_(
                self.model.parameters(),
                self.config.gradient_clip_val
            )
            self.optimizer.step()
            
            # Update metrics
            for k, v in losses.items():
                metrics[k] += v.item()
        
        # Average metrics
        num_batches = len(train_loader)
        return {k: v / num_batches for k, v in metrics.items()}
    
    def _validate(self, val_loader) -> Dict[str, float]:
        """Validate the model."""
        self.model.eval()
        metrics = {
            "total_loss": 0.0,
            "floor_plan_loss": 0.0,
            "elevation_loss": 0.0,
            "specs_loss": 0.0,
            "floor_plan_accuracy": 0.0,
            "elevation_accuracy": 0.0,
            "specs_accuracy": 0.0
        }
        
        with torch.no_grad():
            for inputs, targets in val_loader:
                # Move data to device
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                targets = {k: v.to(self.device) for k, v in targets.items()}
                
                # Forward pass
                outputs = self.model(inputs["features"])
                
                # Calculate losses
                losses = self.criterion(outputs, targets)
                
                # Calculate accuracies
                accuracies = self._calculate_accuracies(outputs, targets)
                
                # Update metrics
                for k, v in losses.items():
                    metrics[k] += v.item()
                for k, v in accuracies.items():
                    metrics[k] += v
        
        # Average metrics
        num_batches = len(val_loader)
        return {k: v / num_batches for k, v in metrics.items()}
    
    def _calculate_accuracies(
        self,
        outputs: Dict[str, torch.Tensor],
        targets: Dict[str, torch.Tensor]
    ) -> Dict[str, float]:
        """Calculate accuracy metrics for each output type."""
        accuracies = {}
        
        # Floor plan accuracy (IoU)
        fp_iou = self._calculate_iou(
            outputs["floor_plans"] > 0.5,
            targets["floor_plans"] > 0.5
        )
        accuracies["floor_plan_accuracy"] = fp_iou.mean().item()
        
        # Elevation accuracy (relative error)
        elev_error = torch.abs(outputs["elevations"] - targets["elevations"])
        accuracies["elevation_accuracy"] = (1 - elev_error.mean()).item()
        
        # Specification accuracy (categorical accuracy)
        spec_pred = outputs["specifications"].argmax(dim=-1)
        spec_target = targets["specifications"].argmax(dim=-1)
        spec_acc = (spec_pred == spec_target).float().mean().item()
        accuracies["specs_accuracy"] = spec_acc
        
        return accuracies
    
    def _calculate_iou(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Calculate Intersection over Union."""
        intersection = (pred & target).float().sum((1, 2))
        union = (pred | target).float().sum((1, 2))
        return intersection / (union + 1e-6)
    
    def _save_checkpoint(self, epoch: int, metrics: Dict[str, float]):
        """Save model checkpoint."""
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "scheduler_state_dict": self.scheduler.state_dict(),
            "metrics": metrics
        }
        
        checkpoint_path = Path(self.config.checkpoint_dir) / f"checkpoint_epoch_{epoch}.pt"
        torch.save(checkpoint, checkpoint_path)
        
        if metrics["total_loss"] < self.best_val_loss:
            best_model_path = Path(self.config.checkpoint_dir) / "best_model.pt"
            torch.save(checkpoint, best_model_path)
            self.best_val_loss = metrics["total_loss"]
    
    def _check_early_stopping(self, val_loss: float) -> bool:
        """Check if training should be stopped early."""
        if val_loss < self.best_val_loss - self.config.min_delta:
            self.best_val_loss = val_loss
            self.patience_counter = 0
        else:
            self.patience_counter += 1
        
        return self.patience_counter >= self.config.patience
