"""Model serving infrastructure for AI services."""

import torch
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from fastapi import BackgroundTasks
import json
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelServer:
    def __init__(self, config: Dict[str, Any]):
        """Initialize model server.
        
        Args:
            config: Server configuration
        """
        self.config = config
        self.models = {}
        self.model_status = {}
        self.model_locks = {}
        self.last_loaded = {}
        
    async def load_model(self, model_name: str) -> bool:
        """Load a model into memory.
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            bool: True if model was loaded successfully
        """
        try:
            async with self._get_model_lock(model_name):
                if self._should_reload_model(model_name):
                    model_path = Path(self.config["model_dir"]) / f"{model_name}.pt"
                    self.models[model_name] = torch.load(
                        model_path,
                        map_location=self.config["device"]
                    )
                    self.models[model_name].eval()
                    self.last_loaded[model_name] = datetime.now()
                    self.model_status[model_name] = "loaded"
                    logger.info(f"Loaded model: {model_name}")
                return True
        except Exception as e:
            self.model_status[model_name] = f"error: {str(e)}"
            logger.error(f"Error loading model {model_name}: {str(e)}")
            return False
            
    async def unload_model(self, model_name: str):
        """Unload a model from memory."""
        async with self._get_model_lock(model_name):
            if model_name in self.models:
                del self.models[model_name]
                self.model_status[model_name] = "unloaded"
                logger.info(f"Unloaded model: {model_name}")
                
    async def get_prediction(
        self,
        model_name: str,
        input_data: Dict[str, Any],
        preprocess_fn: Optional[callable] = None,
        postprocess_fn: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Get prediction from a model.
        
        Args:
            model_name: Name of the model to use
            input_data: Input data for the model
            preprocess_fn: Function to preprocess input data
            postprocess_fn: Function to postprocess model output
            
        Returns:
            Dict containing model outputs
        """
        try:
            # Ensure model is loaded
            if not await self.load_model(model_name):
                raise RuntimeError(f"Failed to load model: {model_name}")
                
            async with self._get_model_lock(model_name):
                # Preprocess input
                if preprocess_fn:
                    input_tensor = preprocess_fn(input_data)
                else:
                    input_tensor = torch.tensor(input_data)
                    
                # Get prediction
                with torch.no_grad():
                    output = self.models[model_name](input_tensor)
                    
                # Postprocess output
                if postprocess_fn:
                    result = postprocess_fn(output)
                else:
                    result = self._default_postprocess(output)
                    
                return {
                    "status": "success",
                    "model": model_name,
                    "timestamp": datetime.now().isoformat(),
                    "result": result
                }
                
        except Exception as e:
            logger.error(f"Error getting prediction from {model_name}: {str(e)}")
            return {
                "status": "error",
                "model": model_name,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            
    def _get_model_lock(self, model_name: str) -> asyncio.Lock:
        """Get or create a lock for a model."""
        if model_name not in self.model_locks:
            self.model_locks[model_name] = asyncio.Lock()
        return self.model_locks[model_name]
        
    def _should_reload_model(self, model_name: str) -> bool:
        """Check if a model should be reloaded."""
        # If model isn't loaded, reload it
        if model_name not in self.models:
            return True
            
        # Check if model file has been updated
        model_path = Path(self.config["model_dir"]) / f"{model_name}.pt"
        if not model_path.exists():
            return False
            
        # Check if model has been loaded recently
        if model_name in self.last_loaded:
            last_load_time = self.last_loaded[model_name]
            model_mtime = datetime.fromtimestamp(model_path.stat().st_mtime)
            return model_mtime > last_load_time
            
        return True
        
    def _default_postprocess(self, output: torch.Tensor) -> Dict[str, Any]:
        """Default postprocessing for model outputs."""
        if isinstance(output, dict):
            return {k: v.cpu().numpy().tolist() for k, v in output.items()}
        elif isinstance(output, torch.Tensor):
            return output.cpu().numpy().tolist()
        else:
            return output
            
    async def get_model_status(self, model_name: str) -> Dict[str, Any]:
        """Get status of a model."""
        return {
            "name": model_name,
            "status": self.model_status.get(model_name, "unknown"),
            "last_loaded": self.last_loaded.get(model_name, None),
            "device": str(next(self.models[model_name].parameters()).device)
            if model_name in self.models else None
        }
        
    async def warmup(self, model_names: List[str]):
        """Warm up specified models by loading them into memory."""
        tasks = [self.load_model(name) for name in model_names]
        await asyncio.gather(*tasks)
        
    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage of loaded models."""
        memory_usage = {}
        for name, model in self.models.items():
            memory_usage[name] = sum(
                p.element_size() * p.nelement()
                for p in model.parameters()
            ) / 1024 / 1024  # Convert to MB
        return memory_usage
