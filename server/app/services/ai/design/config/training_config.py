"""Training configuration for the Design Generator model."""

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TrainingConfig:
    # Model parameters
    batch_size: int = 32
    learning_rate: float = 1e-4
    num_epochs: int = 100
    validation_split: float = 0.2
    
    # Architecture parameters
    input_size: int = 64
    hidden_size: int = 512
    num_layers: int = 6
    num_heads: int = 8
    dropout: float = 0.1
    
    # Loss weights
    floor_plan_loss_weight: float = 1.0
    elevation_loss_weight: float = 1.0
    specs_loss_weight: float = 0.5
    
    # Training devices
    device: str = "cuda"
    num_workers: int = 4
    
    # Checkpointing
    save_every_n_epochs: int = 5
    checkpoint_dir: str = "weights"
    
    # Early stopping
    patience: int = 10
    min_delta: float = 1e-4
    
    # Optimization
    weight_decay: float = 1e-5
    gradient_clip_val: float = 1.0
