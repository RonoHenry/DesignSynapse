"""Base configuration for AI models."""

from pathlib import Path
import torch
import os

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
MODEL_DIR = BASE_DIR / "ai" / "weights"
CACHE_DIR = BASE_DIR / "ai" / "cache"

# Ensure directories exist
MODEL_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Model configurations
MODEL_CONFIGS = {
    "design": {
        "architecture": "transformer",
        "weights": MODEL_DIR / "design_generator.pt",
        "config": {
            "input_size": 512,
            "hidden_size": 768,
            "num_layers": 12,
            "num_heads": 12,
            "dropout": 0.1
        }
    },
    "render": {
        "architecture": "diffusion",
        "weights": MODEL_DIR / "render_processor.pt",
        "config": {
            "image_size": 1024,
            "channels": 3,
            "timesteps": 1000
        }
    },
    "engineering": {
        "architecture": "graph_neural_network",
        "weights": MODEL_DIR / "engineering_calculator.pt",
        "config": {
            "node_features": 64,
            "edge_features": 32,
            "hidden_layers": 8
        }
    },
    "cost": {
        "architecture": "transformer",
        "weights": MODEL_DIR / "cost_estimator.pt",
        "config": {
            "input_size": 256,
            "hidden_size": 512,
            "num_layers": 8,
            "num_heads": 8
        }
    }
}

# Device configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model loading utilities
def get_model_path(model_type: str) -> Path:
    """Get the path to model weights."""
    return MODEL_CONFIGS[model_type]["weights"]

def get_model_config(model_type: str) -> dict:
    """Get the model configuration."""
    return MODEL_CONFIGS[model_type]["config"]
