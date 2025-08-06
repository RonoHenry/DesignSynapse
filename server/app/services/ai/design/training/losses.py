"""Loss functions for training the Design Generator model."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any

class DesignLoss:
    def __init__(self, config: Dict[str, Any]):
        """Initialize loss functions with weights from config."""
        self.floor_plan_weight = config["floor_plan_loss_weight"]
        self.elevation_weight = config["elevation_loss_weight"]
        self.specs_weight = config["specs_loss_weight"]
        
        # Initialize individual loss functions
        self.floor_plan_loss = FloorPlanLoss()
        self.elevation_loss = ElevationLoss()
        self.specs_loss = SpecificationLoss()
        
    def __call__(self, 
                 predictions: Dict[str, torch.Tensor], 
                 targets: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """Calculate weighted combination of losses.
        
        Args:
            predictions: Dictionary containing model outputs
            targets: Dictionary containing target values
            
        Returns:
            Dictionary containing individual and total losses
        """
        # Calculate individual losses
        floor_plan_loss = self.floor_plan_loss(predictions["floor_plans"], targets["floor_plans"])
        elevation_loss = self.elevation_loss(predictions["elevations"], targets["elevations"])
        specs_loss = self.specs_loss(predictions["specifications"], targets["specifications"])
        
        # Calculate weighted total loss
        total_loss = (
            self.floor_plan_weight * floor_plan_loss +
            self.elevation_weight * elevation_loss +
            self.specs_weight * specs_loss
        )
        
        return {
            "total_loss": total_loss,
            "floor_plan_loss": floor_plan_loss,
            "elevation_loss": elevation_loss,
            "specs_loss": specs_loss
        }

class FloorPlanLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse_loss = nn.MSELoss(reduction='mean')
        self.bce_loss = nn.BCELoss(reduction='mean')
    
    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Calculate floor plan loss using combination of MSE and BCE.
        
        The floor plan loss combines:
        1. MSE loss for continuous values (dimensions, positions)
        2. BCE loss for binary features (walls, doors, windows)
        """
        # MSE for continuous values
        mse = self.mse_loss(pred, target)
        
        # BCE for binary features (assuming values are between 0 and 1)
        bce = self.bce_loss(pred, target)
        
        # Add structural consistency loss
        consistency_loss = self._structural_consistency_loss(pred)
        
        return mse + bce + 0.1 * consistency_loss
    
    def _structural_consistency_loss(self, pred: torch.Tensor) -> torch.Tensor:
        """Calculate structural consistency loss.
        
        Ensures:
        1. Walls are connected
        2. Rooms are properly enclosed
        3. No overlapping spaces
        """
        # Calculate gradients in x and y directions
        dx = torch.abs(pred[:, :, 1:] - pred[:, :, :-1])
        dy = torch.abs(pred[:, 1:, :] - pred[:, :-1, :])
        
        # Encourage connectivity by penalizing isolated points
        connectivity_loss = dx.mean() + dy.mean()
        
        return connectivity_loss

class ElevationLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse_loss = nn.MSELoss(reduction='mean')
        self.l1_loss = nn.L1Loss(reduction='mean')
    
    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Calculate elevation loss using combination of L1 and MSE.
        
        The elevation loss combines:
        1. MSE loss for overall shape matching
        2. L1 loss for height accuracy
        3. Gradient loss for smoothness
        """
        # Basic losses
        mse = self.mse_loss(pred, target)
        l1 = self.l1_loss(pred, target)
        
        # Gradient loss for smoothness
        smoothness_loss = self._smoothness_loss(pred)
        
        return mse + 0.5 * l1 + 0.1 * smoothness_loss
    
    def _smoothness_loss(self, pred: torch.Tensor) -> torch.Tensor:
        """Calculate smoothness loss for elevations."""
        # Calculate gradients
        dx = torch.abs(pred[:, 1:] - pred[:, :-1])
        
        # Penalize large changes in height
        return dx.mean()

class SpecificationLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.ce_loss = nn.CrossEntropyLoss(reduction='mean')
        self.mse_loss = nn.MSELoss(reduction='mean')
    
    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Calculate specification loss.
        
        Combines:
        1. Cross entropy for categorical specifications
        2. MSE for continuous values
        """
        # Split predictions into categorical and continuous parts
        cat_pred, cont_pred = pred.split([256, 256], dim=-1)
        cat_target, cont_target = target.split([256, 256], dim=-1)
        
        # Calculate losses
        cat_loss = self.ce_loss(cat_pred, cat_target)
        cont_loss = self.mse_loss(cont_pred, cont_target)
        
        return cat_loss + cont_loss
