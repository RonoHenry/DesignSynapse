"""Data pipeline for processing and managing architectural design data."""

import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from PIL import Image
import pandas as pd
from tqdm import tqdm
import h5py

class ArchitecturalDataPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_dir = Path(config["data_dir"])
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(exist_ok=True)
        
    def process_raw_data(self):
        """Process raw architectural data into training format."""
        # Process floor plans
        self._process_floor_plans()
        # Process elevations
        self._process_elevations()
        # Process specifications
        self._process_specifications()
        # Create dataset index
        self._create_dataset_index()
        
    def _process_floor_plans(self):
        """Process floor plan images and annotations."""
        floor_plans_dir = self.data_dir / "raw" / "floor_plans"
        processed_dir = self.processed_dir / "floor_plans"
        processed_dir.mkdir(exist_ok=True)
        
        for plan_path in tqdm(list(floor_plans_dir.glob("*.png"))):
            # Load floor plan image
            plan = Image.open(plan_path)
            # Load annotations
            anno_path = floor_plans_dir / "annotations" / f"{plan_path.stem}.json"
            with open(anno_path, 'r') as f:
                annotations = json.load(f)
                
            # Process floor plan
            processed_plan = self._preprocess_floor_plan(plan, annotations)
            
            # Save processed data
            np.save(
                processed_dir / f"{plan_path.stem}.npy",
                processed_plan
            )
            
    def _process_elevations(self):
        """Process elevation drawings and height data."""
        elevations_dir = self.data_dir / "raw" / "elevations"
        processed_dir = self.processed_dir / "elevations"
        processed_dir.mkdir(exist_ok=True)
        
        for elev_path in tqdm(list(elevations_dir.glob("*.png"))):
            # Load elevation drawing
            elevation = Image.open(elev_path)
            # Load height data
            height_path = elevations_dir / "height_data" / f"{elev_path.stem}.json"
            with open(height_path, 'r') as f:
                height_data = json.load(f)
                
            # Process elevation
            processed_elevation = self._preprocess_elevation(elevation, height_data)
            
            # Save processed data
            np.save(
                processed_dir / f"{elev_path.stem}.npy",
                processed_elevation
            )
            
    def _process_specifications(self):
        """Process building specifications and requirements."""
        specs_dir = self.data_dir / "raw" / "specifications"
        processed_dir = self.processed_dir / "specifications"
        processed_dir.mkdir(exist_ok=True)
        
        # Load specifications dataset
        specs_df = pd.read_csv(specs_dir / "specifications.csv")
        
        for _, row in tqdm(specs_df.iterrows()):
            # Process specifications
            processed_specs = self._preprocess_specifications(row)
            
            # Save processed data
            np.save(
                processed_dir / f"{row['design_id']}.npy",
                processed_specs
            )
            
    def _create_dataset_index(self):
        """Create index of processed dataset."""
        index = {
            "train": [],
            "val": [],
            "test": []
        }
        
        # Get all processed designs
        designs = list(self.processed_dir.glob("*/*.npy"))
        
        # Random split
        np.random.shuffle(designs)
        n_designs = len(designs)
        n_train = int(0.7 * n_designs)
        n_val = int(0.15 * n_designs)
        
        index["train"] = [d.stem for d in designs[:n_train]]
        index["val"] = [d.stem for d in designs[n_train:n_train+n_val]]
        index["test"] = [d.stem for d in designs[n_train+n_val:]]
        
        # Save index
        with open(self.processed_dir / "index.json", 'w') as f:
            json.dump(index, f)
            
    def _preprocess_floor_plan(self, 
                             plan: Image.Image, 
                             annotations: Dict[str, Any]) -> np.ndarray:
        """Preprocess floor plan image and annotations."""
        # Convert image to numpy array
        plan_array = np.array(plan)
        
        # Extract room layouts
        rooms = self._extract_room_layouts(plan_array, annotations)
        
        # Extract wall positions
        walls = self._extract_wall_positions(plan_array, annotations)
        
        # Combine features
        features = np.concatenate([
            rooms,
            walls,
            self._create_spatial_encoding(plan_array.shape)
        ], axis=-1)
        
        return features
        
    def _preprocess_elevation(self, 
                            elevation: Image.Image, 
                            height_data: Dict[str, Any]) -> np.ndarray:
        """Preprocess elevation drawing and height data."""
        # Convert image to numpy array
        elev_array = np.array(elevation)
        
        # Extract height profile
        height_profile = self._extract_height_profile(elev_array, height_data)
        
        # Extract architectural features
        features = self._extract_architectural_features(elev_array)
        
        # Combine features
        processed = np.concatenate([
            height_profile,
            features,
            self._create_vertical_encoding(elev_array.shape)
        ], axis=-1)
        
        return processed
        
    def _preprocess_specifications(self, 
                                 specs_row: pd.Series) -> np.ndarray:
        """Preprocess building specifications."""
        # Extract numerical features
        numerical = np.array([
            specs_row["area"],
            specs_row["height"],
            specs_row["num_floors"],
            specs_row["energy_rating"]
        ])
        
        # One-hot encode categorical features
        categorical = self._one_hot_encode_specs(specs_row)
        
        # Combine features
        return np.concatenate([numerical, categorical])
        
    def _extract_room_layouts(self, 
                            plan: np.ndarray, 
                            annotations: Dict[str, Any]) -> np.ndarray:
        """Extract room layout features from floor plan."""
        room_features = np.zeros((*plan.shape[:2], len(self.config["room_types"])))
        
        for room in annotations["rooms"]:
            room_type = room["type"]
            mask = self._create_room_mask(room["coordinates"], plan.shape[:2])
            room_idx = self.config["room_types"].index(room_type)
            room_features[:, :, room_idx] = mask
            
        return room_features
        
    def _extract_wall_positions(self, 
                              plan: np.ndarray, 
                              annotations: Dict[str, Any]) -> np.ndarray:
        """Extract wall position features from floor plan."""
        wall_features = np.zeros((*plan.shape[:2], 2))  # Horizontal and vertical walls
        
        for wall in annotations["walls"]:
            start, end = wall["start"], wall["end"]
            if start[0] == end[0]:  # Vertical wall
                wall_features[min(start[1], end[1]):max(start[1], end[1]), start[0], 0] = 1
            else:  # Horizontal wall
                wall_features[start[1], min(start[0], end[0]):max(start[0], end[0]), 1] = 1
                
        return wall_features
        
    def _create_spatial_encoding(self, shape: Tuple[int, int]) -> np.ndarray:
        """Create spatial position encoding."""
        h, w = shape[:2]
        x = np.linspace(-1, 1, w)
        y = np.linspace(-1, 1, h)
        xv, yv = np.meshgrid(x, y)
        return np.stack([xv, yv], axis=-1)
        
    def _create_vertical_encoding(self, shape: Tuple[int, int]) -> np.ndarray:
        """Create vertical position encoding for elevations."""
        h, w = shape[:2]
        y = np.linspace(0, 1, h)
        return np.tile(y[:, np.newaxis], (1, w))
        
    def _one_hot_encode_specs(self, specs_row: pd.Series) -> np.ndarray:
        """One-hot encode categorical specification features."""
        categorical_features = []
        
        for feature in self.config["categorical_features"]:
            values = self.config["feature_values"][feature]
            encoding = np.zeros(len(values))
            if specs_row[feature] in values:
                encoding[values.index(specs_row[feature])] = 1
            categorical_features.append(encoding)
            
        return np.concatenate(categorical_features)
