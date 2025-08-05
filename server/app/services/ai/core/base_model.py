"""Base model class for all AI models."""

from abc import ABC, abstractmethod
import torch
from typing import Any, Dict
from pathlib import Path
from app.services.ai.core.config import DEVICE

class BaseModel(ABC):
    def __init__(self, model_path: Path, model_config: Dict[str, Any]):
        self.model_path = model_path
        self.model_config = model_config
        self.model = None
        self.device = DEVICE

    @abstractmethod
    def load_model(self):
        """Load model from disk."""
        pass

    @abstractmethod
    def preprocess(self, input_data: Dict[str, Any]) -> Any:
        """Preprocess input data before model inference."""
        pass

    @abstractmethod
    def postprocess(self, model_output: Any) -> Dict[str, Any]:
        """Postprocess model output into desired format."""
        pass

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data before processing."""
        pass

    def ensure_model_loaded(self):
        """Ensure model is loaded before inference."""
        if self.model is None:
            self.load_model()

    async def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run model inference pipeline."""
        # Validate input
        if not self.validate_input(input_data):
            raise ValueError("Invalid input data")

        # Ensure model is loaded
        self.ensure_model_loaded()

        # Preprocess
        processed_input = self.preprocess(input_data)

        # Move to correct device
        if isinstance(processed_input, torch.Tensor):
            processed_input = processed_input.to(self.device)

        # Run inference
        with torch.no_grad():
            output = self.model(processed_input)

        # Postprocess
        result = self.postprocess(output)

        return result
