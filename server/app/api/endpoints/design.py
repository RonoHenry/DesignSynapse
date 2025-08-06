"""API endpoints for design generation and management."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from pathlib import Path
import torch
from app.services.ai.design.model import DesignGenerator
from app.core.config import get_settings

router = APIRouter(prefix="/api/design", tags=["design"])

class DesignRequest(BaseModel):
    """Design generation request model."""
    area: float
    width: float
    length: float
    height: Optional[float] = None
    rooms: Dict[str, int]
    style: str
    needs_garage: Optional[bool] = False
    needs_basement: Optional[bool] = False
    sustainable_design: Optional[bool] = False

class DesignResponse(BaseModel):
    """Design generation response model."""
    design_id: str
    floor_plans: Dict[str, Any]
    elevations: Dict[str, Any]
    specifications: Dict[str, Any]
    metadata: Dict[str, Any]

# Initialize the design generator
generator = DesignGenerator()

@router.post("/generate", response_model=DesignResponse)
async def generate_design(request: DesignRequest, background_tasks: BackgroundTasks):
    """Generate a new architectural design."""
    try:
        # Validate input
        if not generator.validate_input(request.dict()):
            raise HTTPException(status_code=400, message="Invalid input parameters")

        # Preprocess input
        input_tensor = generator.preprocess(request.dict())

        # Generate design
        with torch.no_grad():
            output = generator.model(input_tensor)

        # Postprocess output
        design_data = generator.postprocess(output)

        # Generate unique design ID
        design_id = generate_unique_id()

        # Save design data
        background_tasks.add_task(save_design_data, design_id, design_data)

        return DesignResponse(
            design_id=design_id,
            **design_data,
            metadata={
                "input_parameters": request.dict(),
                "generation_timestamp": datetime.now().isoformat()
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/design/{design_id}", response_model=DesignResponse)
async def get_design(design_id: str):
    """Retrieve a generated design by ID."""
    try:
        design_data = load_design_data(design_id)
        if not design_data:
            raise HTTPException(status_code=404, detail="Design not found")
        return design_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/design/{design_id}/modify")
async def modify_design(design_id: str, modifications: Dict[str, Any]):
    """Modify an existing design."""
    try:
        # Load existing design
        design_data = load_design_data(design_id)
        if not design_data:
            raise HTTPException(status_code=404, detail="Design not found")

        # Apply modifications
        modified_data = apply_design_modifications(design_data, modifications)

        # Save modified design
        save_design_data(design_id, modified_data)

        return modified_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train")
async def trigger_training(background_tasks: BackgroundTasks):
    """Trigger model training in the background."""
    try:
        background_tasks.add_task(train_model)
        return {"message": "Training started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Utility functions
def generate_unique_id() -> str:
    """Generate a unique ID for a design."""
    import uuid
    return str(uuid.uuid4())

def save_design_data(design_id: str, data: Dict[str, Any]):
    """Save design data to storage."""
    storage_path = Path(get_settings().DESIGN_STORAGE_PATH) / design_id
    storage_path.mkdir(parents=True, exist_ok=True)

    # Save different components
    torch.save(data["floor_plans"], storage_path / "floor_plans.pt")
    torch.save(data["elevations"], storage_path / "elevations.pt")
    
    # Save metadata
    with open(storage_path / "metadata.json", "w") as f:
        json.dump(data["metadata"], f)

def load_design_data(design_id: str) -> Optional[Dict[str, Any]]:
    """Load design data from storage."""
    storage_path = Path(get_settings().DESIGN_STORAGE_PATH) / design_id
    if not storage_path.exists():
        return None

    data = {
        "floor_plans": torch.load(storage_path / "floor_plans.pt"),
        "elevations": torch.load(storage_path / "elevations.pt"),
    }

    # Load metadata
    with open(storage_path / "metadata.json", "r") as f:
        data["metadata"] = json.load(f)

    return data

def apply_design_modifications(design_data: Dict[str, Any], 
                             modifications: Dict[str, Any]) -> Dict[str, Any]:
    """Apply modifications to an existing design."""
    # TODO: Implement design modification logic
    modified_data = design_data.copy()
    # Apply modifications here
    return modified_data

def train_model():
    """Run model training."""
    from app.services.ai.design.training.trainer import Trainer
    from app.services.ai.design.config.training_config import TrainingConfig

    config = TrainingConfig()
    trainer = Trainer(config)
    trainer.train(Path(get_settings().TRAINING_DATA_PATH))
