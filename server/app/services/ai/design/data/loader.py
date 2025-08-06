"""Data loading utilities for architectural designs."""

import torch
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import numpy as np
from typing import Dict, Any, Tuple, List
import json

class ArchitecturalDataset(Dataset):
    def __init__(self, data_dir: Path, split: str = "train"):
        """
        Args:
            data_dir (Path): Directory containing the dataset
            split (str): Either 'train' or 'val'
        """
        self.data_dir = data_dir
        self.split = split
        
        # Load dataset index
        index_path = data_dir / f"{split}_index.json"
        with open(index_path, "r") as f:
            self.data_index = json.load(f)
            
        # Load design parameters
        params_path = data_dir / "design_params.json"
        with open(params_path, "r") as f:
            self.design_params = json.load(f)
    
    def __len__(self) -> int:
        return len(self.data_index)
    
    def __getitem__(self, idx: int) -> Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]:
        """Get a single training example.
        
        Returns:
            Tuple containing:
                - Input features dictionary
                - Target outputs dictionary
        """
        design_id = self.data_index[idx]
        design_path = self.data_dir / design_id
        
        # Load input features
        input_features = self._load_input_features(design_path)
        
        # Load target outputs
        target_outputs = self._load_target_outputs(design_path)
        
        return input_features, target_outputs
    
    def _load_input_features(self, design_path: Path) -> Dict[str, torch.Tensor]:
        """Load input features for a design."""
        with open(design_path / "requirements.json", "r") as f:
            requirements = json.load(f)
        
        # Convert requirements to tensor format
        features = []
        
        # Dimensions
        features.extend([
            requirements["area"] / self.design_params["max_area"],
            requirements["width"] / self.design_params["max_dimension"],
            requirements["length"] / self.design_params["max_dimension"],
            requirements.get("height", 3.0) / self.design_params["max_height"]
        ])
        
        # Room counts
        room_counts = requirements.get("rooms", {})
        for room_type in ["bedrooms", "bathrooms", "living_rooms", "kitchens"]:
            count = room_counts.get(room_type, 0)
            features.append(count / self.design_params["max_rooms"])
        
        # Style (one-hot encoded)
        style_idx = self.design_params["styles"].index(requirements.get("style", "modern"))
        style_vector = [1.0 if i == style_idx else 0.0 for i in range(len(self.design_params["styles"]))]
        features.extend(style_vector)
        
        # Additional features
        features.extend([
            float(requirements.get("needs_garage", False)),
            float(requirements.get("needs_basement", False)),
            float(requirements.get("sustainable_design", False))
        ])
        
        return {"features": torch.tensor(features, dtype=torch.float32)}
    
    def _load_target_outputs(self, design_path: Path) -> Dict[str, torch.Tensor]:
        """Load target outputs for a design."""
        # Load floor plan
        floor_plan = np.load(design_path / "floor_plan.npy")
        
        # Load elevations
        elevations = np.load(design_path / "elevations.npy")
        
        # Load specifications
        with open(design_path / "specifications.json", "r") as f:
            specs = json.load(f)
        spec_vector = self._convert_specs_to_vector(specs)
        
        return {
            "floor_plans": torch.tensor(floor_plan, dtype=torch.float32),
            "elevations": torch.tensor(elevations, dtype=torch.float32),
            "specifications": torch.tensor(spec_vector, dtype=torch.float32)
        }
    
    def _convert_specs_to_vector(self, specs: Dict[str, Any]) -> np.ndarray:
        """Convert specifications dictionary to vector format."""
        vector = []
        
        # Materials (one-hot encoded)
        materials_vector = [0.0] * len(self.design_params["materials"])
        for material in specs.get("materials", []):
            if material in self.design_params["materials"]:
                idx = self.design_params["materials"].index(material)
                materials_vector[idx] = 1.0
        vector.extend(materials_vector)
        
        # Construction details
        vector.extend([
            float(specs.get("floor_height", 3.0)) / self.design_params["max_floor_height"],
            float(specs.get("wall_thickness", 0.3)) / self.design_params["max_wall_thickness"]
        ])
        
        # Technical requirements
        tech_req = specs.get("technical_requirements", {})
        vector.extend([
            float(tech_req.get("energy_rating", 0)) / 100.0,
            float(tech_req.get("acoustic_rating", 0)) / 100.0,
            float(tech_req.get("thermal_rating", 0)) / 100.0
        ])
        
        return np.array(vector, dtype=np.float32)

def create_data_loaders(
    data_dir: Path,
    batch_size: int,
    num_workers: int,
    validation_split: float = 0.2
) -> Tuple[DataLoader, DataLoader]:
    """Create training and validation data loaders.
    
    Args:
        data_dir: Directory containing the dataset
        batch_size: Batch size for training
        num_workers: Number of worker processes for data loading
        validation_split: Fraction of data to use for validation
        
    Returns:
        Tuple containing:
            - Training data loader
            - Validation data loader
    """
    # Create datasets
    train_dataset = ArchitecturalDataset(data_dir, split="train")
    val_dataset = ArchitecturalDataset(data_dir, split="val")
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader
