from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.db.database import get_db
from app.services.ai.design.generator import DesignGenerator
from app.services.ai.render.processor import RenderProcessor
from app.services.ai.engineering.calculator import EngineeringCalculator
from app.services.ai.cost.estimator import CostEstimator

router = APIRouter()

@router.post("/design/generate", response_model=Dict[str, Any])
async def generate_design(
    requirements: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Generate architectural design based on requirements.
    
    Parameters:
    - requirements: Dict containing design parameters and constraints
    """
    try:
        generator = DesignGenerator()
        result = await generator.generate(requirements)
        return {"status": "success", "design": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/render/process", response_model=Dict[str, Any])
async def process_render(
    model_data: Dict[str, Any],
    render_settings: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Process 3D model for rendering with specified settings.
    
    Parameters:
    - model_data: Dict containing 3D model information
    - render_settings: Dict containing rendering parameters
    """
    try:
        processor = RenderProcessor()
        result = await processor.process(model_data, render_settings)
        return {"status": "success", "render": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/engineering/calculate", response_model=Dict[str, Any])
async def calculate_engineering(
    design_data: Dict[str, Any],
    calculation_type: str,
    db: Session = Depends(get_db)
):
    """
    Perform engineering calculations on design data.
    
    Parameters:
    - design_data: Dict containing design specifications
    - calculation_type: Type of engineering calculation to perform
    """
    try:
        calculator = EngineeringCalculator()
        result = await calculator.calculate(design_data, calculation_type)
        return {"status": "success", "calculations": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cost/estimate", response_model=Dict[str, Any])
async def estimate_cost(
    project_data: Dict[str, Any],
    estimate_type: str,
    db: Session = Depends(get_db)
):
    """
    Generate cost estimates for project.
    
    Parameters:
    - project_data: Dict containing project specifications
    - estimate_type: Type of cost estimation to perform
    """
    try:
        estimator = CostEstimator()
        result = await estimator.estimate(project_data, estimate_type)
        return {"status": "success", "estimate": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
