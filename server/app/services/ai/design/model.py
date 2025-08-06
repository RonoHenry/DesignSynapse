"""Design Generator model implementation."""

import torch
import torch.nn as nn
import math
import numpy as np
from typing import Dict, Any, Tuple, List
from datetime import datetime
from dataclasses import dataclass
from app.services.ai.core.exceptions import ModelProcessingError

@dataclass
class DesignInputValidation:
    """Validation rules for design input parameters."""
    min_area: float = 20.0  # Minimum area in square meters
    max_area: float = 1000.0  # Maximum area in square meters
    min_dimension: float = 3.0  # Minimum width/length in meters
    max_dimension: float = 100.0  # Maximum width/length in meters
    min_height: float = 2.4  # Minimum ceiling height in meters
    max_height: float = 30.0  # Maximum building height in meters
    max_rooms_per_type: int = 10  # Maximum number of rooms of each type
    valid_styles: List[str] = ["modern", "traditional", "minimalist", "industrial"]

@dataclass
class DesignParameters:
    """Container for validated design parameters."""
    area: float
    width: float
    length: float
    height: float
    rooms: Dict[str, int]
    style: str
    additional_features: Dict[str, bool]

    @classmethod
    def from_dict(cls, data: Dict[str, Any], validation: DesignInputValidation) -> 'DesignParameters':
        """Create validated design parameters from input dictionary."""
        # Validate dimensions
        area = cls._validate_range(data.get("area", 0), 
                                 validation.min_area, 
                                 validation.max_area, 
                                 "area")
        width = cls._validate_range(data.get("width", 0), 
                                  validation.min_dimension, 
                                  validation.max_dimension, 
                                  "width")
        length = cls._validate_range(data.get("length", 0), 
                                   validation.min_dimension, 
                                   validation.max_dimension, 
                                   "length")
        height = cls._validate_range(data.get("height", validation.min_height), 
                                   validation.min_height, 
                                   validation.max_height, 
                                   "height")

        # Validate rooms
        rooms = data.get("rooms", {})
        validated_rooms = {}
        for room_type, count in rooms.items():
            if count < 0:
                raise ValueError(f"Room count cannot be negative: {room_type}")
            if count > validation.max_rooms_per_type:
                raise ValueError(f"Too many {room_type}: {count} (max {validation.max_rooms_per_type})")
            validated_rooms[room_type] = count

        # Validate style
        style = data.get("style", "modern")
        if style not in validation.valid_styles:
            raise ValueError(f"Invalid style: {style}. Must be one of: {validation.valid_styles}")

        # Additional features
        additional_features = {
            "needs_garage": bool(data.get("needs_garage", False)),
            "needs_basement": bool(data.get("needs_basement", False)),
            "sustainable_design": bool(data.get("sustainable_design", False))
        }

        return cls(
            area=area,
            width=width,
            length=length,
            height=height,
            rooms=validated_rooms,
            style=style,
            additional_features=additional_features
        )

    @staticmethod
    def _validate_range(value: float, min_val: float, max_val: float, field_name: str) -> float:
        """Validate that a value falls within the acceptable range."""
        if value < min_val:
            raise ValueError(f"{field_name} cannot be less than {min_val}")
        if value > max_val:
            raise ValueError(f"{field_name} cannot be more than {max_val}")
        return value
from pathlib import Path
from app.services.ai.core.base_model import BaseModel
from app.services.ai.core.config import get_model_path, get_model_config

class DesignGeneratorModel(nn.Module):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.input_size = config["input_size"]
        self.hidden_size = config["hidden_size"]
        self.num_layers = config["num_layers"]
        self.num_heads = config["num_heads"]
        
        # Embedding layer
        self.embedding = nn.Linear(self.input_size, self.hidden_size)
        
        # Transformer layers
        self.transformer_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=self.hidden_size,
                nhead=self.num_heads,
                dim_feedforward=self.hidden_size * 4,
                dropout=config["dropout"]
            ) for _ in range(self.num_layers)
        ])
        
        # Output layers
        self.floor_plan_decoder = nn.Linear(self.hidden_size, 2048)  # Floor plan generation
        self.elevation_decoder = nn.Linear(self.hidden_size, 1024)   # Elevation generation
        self.specs_decoder = nn.Linear(self.hidden_size, 512)        # Specifications generation

    def forward(self, x):
        """Forward pass of the model.
        
        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, input_size)
            
        Returns:
            dict: Dictionary containing generated design elements
        """
        if x.dim() != 2 or x.size(1) != self.input_size:
            raise ValueError(f"Expected input shape (batch_size, {self.input_size}), got {x.shape}")
        
        # Embed input
        x = self.embedding(x)  # Shape: (batch_size, hidden_size)
        
        # Add positional encoding for transformer
        batch_size = x.size(0)
        pos_encoding = self.create_positional_encoding(batch_size)
        x = x + pos_encoding.to(x.device)
        
        # Apply transformer layers with attention mask
        attention_mask = self.create_attention_mask(batch_size)
        for layer in self.transformer_layers:
            x = layer(x, src_key_padding_mask=attention_mask)
        
        # Generate different aspects of the design with activation functions
        floor_plans = torch.sigmoid(self.floor_plan_decoder(x))  # Normalized spatial layout
        elevations = torch.tanh(self.elevation_decoder(x))      # Height information
        specs = torch.softmax(self.specs_decoder(x), dim=-1)    # Categorical specifications
        
        return {
            "floor_plans": floor_plans,
            "elevations": elevations,
            "specifications": specs
        }
        
    def create_positional_encoding(self, batch_size):
        """Create positional encoding for transformer input."""
        pos_encoding = torch.zeros(batch_size, self.hidden_size)
        position = torch.arange(0, batch_size, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, self.hidden_size, 2).float() * (-math.log(10000.0) / self.hidden_size))
        pos_encoding[:, 0::2] = torch.sin(position * div_term)
        pos_encoding[:, 1::2] = torch.cos(position * div_term)
        return pos_encoding
        
    def create_attention_mask(self, batch_size):
        """Create attention mask for transformer layers."""
        return torch.zeros(batch_size, dtype=torch.bool)

class DesignGenerator(BaseModel):
    def __init__(self):
        model_path = get_model_path("design")
        model_config = get_model_config("design")
        super().__init__(model_path, model_config)

    def load_model(self):
        """Load the design generator model."""
        self.model = DesignGeneratorModel(self.model_config)
        if self.model_path.exists():
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def preprocess(self, input_data: Dict[str, Any]) -> torch.Tensor:
        """Convert input requirements to model-ready format with validation.
        
        Args:
            input_data (Dict[str, Any]): Raw input data containing design requirements
            
        Returns:
            torch.Tensor: Preprocessed tensor ready for model input
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Validate required fields
        required_fields = ["area", "width", "length"]
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
            
        # Validate numerical constraints
        for field in ["area", "width", "length", "height"]:
            value = input_data.get(field, 0)
            if value < 0:
                raise ValueError(f"{field} cannot be negative")
            if field != "height" and value == 0:
                raise ValueError(f"{field} cannot be zero")
                
        features = []
        
        # Normalize dimensions to reasonable ranges
        max_area = 1000  # 1000 sq meters as max reference
        max_dimension = 100  # 100 meters as max reference
        
        features.extend([
            min(input_data.get("area", 0) / max_area, 1.0),
            min(input_data.get("width", 0) / max_dimension, 1.0),
            min(input_data.get("length", 0) / max_dimension, 1.0),
            min(input_data.get("height", 0) / max_dimension, 1.0) if input_data.get("height") else 0.0
        ])
        
        # Validate and normalize room requirements
        room_counts = input_data.get("rooms", {})
        max_rooms = 10  # Maximum reasonable number of rooms per type
        
        for room_type in ["bedrooms", "bathrooms", "living_rooms", "kitchens"]:
            count = room_counts.get(room_type, 0)
            if count < 0:
                raise ValueError(f"{room_type} count cannot be negative")
            features.append(min(count / max_rooms, 1.0))
        
        # Style preferences with validation
        valid_styles = ["modern", "traditional", "minimalist", "industrial"]
        style = input_data.get("style", "modern")
        if style not in valid_styles:
            raise ValueError(f"Invalid style. Must be one of: {valid_styles}")
            
        style_vector = [1.0 if style == s else 0.0 for s in valid_styles]
        features.extend(style_vector)
        
        # Additional features for constraints and requirements
        features.extend([
            float(input_data.get("needs_garage", False)),
            float(input_data.get("needs_basement", False)),
            float(input_data.get("sustainable_design", False))
        ])
        
        # Convert to tensor with proper shape and normalization
        tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
        
        # Ensure correct input size
        if len(features) > self.model_config["input_size"]:
            raise ValueError(f"Too many features: got {len(features)}, maximum is {self.model_config['input_size']}")
            
        padded = torch.zeros((1, self.model_config["input_size"]))  # Include batch dimension
        padded[0, :len(features)] = tensor
        
        return padded
        
    def postprocess(self, model_output: Dict[str, torch.Tensor], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process model outputs into usable design specifications.
        
        Args:
            model_output (Dict[str, torch.Tensor]): Raw model outputs
            input_data (Dict[str, Any]): Original input data for reference
            
        Returns:
            Dict[str, Any]: Processed design specifications
        """
        try:
            # Convert tensors to numpy for processing
            floor_plans = model_output["floor_plans"].squeeze(0).cpu().numpy()
            elevations = model_output["elevations"].squeeze(0).cpu().numpy()
            specs = model_output["specifications"].squeeze(0).cpu().numpy()
            
            # Process floor plan data
            processed_floor_plan = self._process_floor_plan(floor_plans, input_data)
            
            # Process elevation data
            processed_elevations = self._process_elevations(elevations, input_data)
            
            # Process specifications
            processed_specs = self._process_specifications(specs, input_data)
            
            return {
                "floor_plan": processed_floor_plan,
                "elevations": processed_elevations,
                "specifications": processed_specs,
                "metadata": {
                    "generation_timestamp": datetime.now().isoformat(),
                    "model_version": self.model_config.get("version", "1.0"),
                    "input_parameters": input_data
                }
            }
            
        except Exception as e:
            raise ModelProcessingError(f"Error in postprocessing: {str(e)}")
            
    def _process_floor_plan(self, floor_plan_data: np.ndarray, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert raw floor plan data into structured layout information."""
        # Get actual dimensions from input data
        width = input_data.get("width", 0)
        length = input_data.get("length", 0)
        
        # Reshape floor plan data into 2D grid
        grid_size = int(np.sqrt(len(floor_plan_data)))
        layout_grid = floor_plan_data[:grid_size * grid_size].reshape(grid_size, grid_size)
        
        # Scale to actual dimensions
        x_scale = width / grid_size
        y_scale = length / grid_size
        
        # Process room layout
        rooms = self._detect_rooms(layout_grid)
        
        return {
            "layout_grid": layout_grid.tolist(),
            "dimensions": {
                "width": width,
                "length": length,
                "grid_size": grid_size,
                "scale_factors": {"x": x_scale, "y": y_scale}
            },
            "rooms": rooms
        }
        
    def _process_elevations(self, elevation_data: np.ndarray, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process elevation data into height profiles and 3D information."""
        height = input_data.get("height", 3.0)  # Default ceiling height
        
        return {
            "height_profile": elevation_data.tolist(),
            "max_height": height,
            "sections": self._generate_sections(elevation_data, height)
        }
        
    def _process_specifications(self, specs_data: np.ndarray, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert raw specifications into structured building requirements."""
        # Map specification indices to actual requirements
        spec_categories = [
            "materials", "lighting", "ventilation", "utilities",
            "accessibility", "sustainability", "safety"
        ]
        
        processed_specs = {}
        for i, category in enumerate(spec_categories):
            if i < len(specs_data):
                processed_specs[category] = self._interpret_spec(specs_data[i], category)
                
        return processed_specs
        
    def _detect_rooms(self, layout_grid: np.ndarray) -> List[Dict[str, Any]]:
        """Detect and classify rooms from the layout grid."""
        rooms = []
        visited = np.zeros_like(layout_grid, dtype=bool)
        
        for i in range(layout_grid.shape[0]):
            for j in range(layout_grid.shape[1]):
                if not visited[i, j] and layout_grid[i, j] > 0.5:
                    # Found a new room
                    room_points = self._flood_fill(layout_grid, visited, i, j)
                    room_type = self._classify_room(layout_grid, room_points)
                    rooms.append({
                        "type": room_type,
                        "area": len(room_points),
                        "coordinates": room_points
                    })
                    
        return rooms
        
    def _flood_fill(self, grid: np.ndarray, visited: np.ndarray, i: int, j: int) -> List[Tuple[int, int]]:
        """Flood fill algorithm to find connected room areas."""
        if (i < 0 or i >= grid.shape[0] or j < 0 or j >= grid.shape[1] or 
            visited[i, j] or grid[i, j] < 0.5):
            return []
            
        visited[i, j] = True
        points = [(i, j)]
        
        # Check all adjacent cells
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            points.extend(self._flood_fill(grid, visited, i + di, j + dj))
            
        return points
        
    def _classify_room(self, grid: np.ndarray, points: List[Tuple[int, int]]) -> str:
        """Classify room type based on size and location patterns."""
        area = len(points)
        relative_position = np.mean(points, axis=0) / grid.shape[0]
        
        # Simple classification based on area and position
        if area > grid.shape[0] * grid.shape[1] * 0.2:
            return "living_room"
        elif area > grid.shape[0] * grid.shape[1] * 0.15:
            return "bedroom"
        elif area < grid.shape[0] * grid.shape[1] * 0.05:
            return "bathroom"
        else:
            return "other"
            
    def _generate_sections(self, elevation_data: np.ndarray, max_height: float) -> List[Dict[str, Any]]:
        """Generate building sections from elevation data."""
        sections = []
        section_points = (elevation_data * max_height).tolist()
        
        return [{
            "profile": section_points,
            "max_height": max_height,
            "num_points": len(section_points)
        }]
        
    def _interpret_spec(self, spec_value: float, category: str) -> Dict[str, Any]:
        """Interpret specification values for different categories."""
        if category == "materials":
            materials = ["concrete", "wood", "steel", "glass"]
            material_probs = self._softmax(spec_value * np.ones(len(materials)))
            return {"materials": dict(zip(materials, material_probs.tolist()))}
            
        elif category == "sustainability":
            features = ["solar_panels", "rainwater_harvesting", "natural_ventilation"]
            return {feature: bool(spec_value > 0.5) for feature in features}
            
        else:
            return {"value": float(spec_value), "category": category}
            
    @staticmethod
    def _softmax(x: np.ndarray) -> np.ndarray:
        """Compute softmax values for array of numbers."""
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum().unsqueeze(0)  # Add batch dimension

    def postprocess(self, model_output: Dict[str, torch.Tensor]) -> Dict[str, Any]:
        """Convert model output to usable design data."""
        floor_plans = model_output["floor_plans"].squeeze(0)
        elevations = model_output["elevations"].squeeze(0)
        specs = model_output["specifications"].squeeze(0)
        
        # Convert tensors to design data
        return {
            "floor_plans": self._process_floor_plans(floor_plans),
            "elevations": self._process_elevations(elevations),
            "specifications": self._process_specifications(specs)
        }

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input requirements."""
        required_fields = ["area", "rooms"]
        if not all(field in input_data for field in required_fields):
            return False
        
        if input_data["area"] <= 0:
            return False
        
        if not isinstance(input_data["rooms"], dict):
            return False
            
        return True

    def _process_floor_plans(self, floor_plans: torch.Tensor) -> Dict[str, Any]:
        """Convert floor plan tensor to structured data."""
        # TODO: Implement floor plan processing
        return {
            "layout": floor_plans.cpu().numpy().tolist(),
            "scale": "1:100",
            "dimensions": {
                "width": 10.0,
                "length": 15.0
            }
        }

    def _process_elevations(self, elevations: torch.Tensor) -> Dict[str, Any]:
        """Convert elevation tensor to structured data."""
        # TODO: Implement elevation processing
        return {
            "views": {
                "front": elevations[:256].cpu().numpy().tolist(),
                "back": elevations[256:512].cpu().numpy().tolist(),
                "left": elevations[512:768].cpu().numpy().tolist(),
                "right": elevations[768:].cpu().numpy().tolist()
            }
        }

    def _process_specifications(self, specs: torch.Tensor) -> Dict[str, Any]:
        """Convert specifications tensor to structured data."""
        # TODO: Implement specifications processing
        return {
            "materials": [],
            "construction_details": {},
            "technical_requirements": {}
        }
