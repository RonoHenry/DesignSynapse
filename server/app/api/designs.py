"""Design-related API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List
from ..services.validation import ValidationService
from ..services.ai.render.processor import RenderProcessor
from ..db.models import Design, User
from ..schemas.design import (
    DesignCreate,
    DesignUpdate,
    DesignResponse,
    DesignValidationRequest,
    DesignValidationResponse
)
from ..core.auth import get_current_user
from ..core.errors import ValidationError

router = APIRouter(prefix="/designs", tags=["designs"])
validation_service = ValidationService()
render_processor = RenderProcessor()

@router.post("/", response_model=DesignResponse)
async def create_design(
    design: DesignCreate,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Create a new design."""
    try:
        # Validate design first
        validation = await validation_service.validate_design(design.dict())
        if not validation["valid"]:
            raise ValidationError("Design validation failed", details=validation["issues"])
            
        # Create design in DB
        design_db = await Design.create(**design.dict(), user_id=current_user.id)
        
        # Generate initial preview
        preview = await render_processor.process(
            design_db.model_data,
            {"resolution": "preview"}
        )
        
        # Update design with preview
        design_db.preview_data = preview
        await design_db.save()
        
        return design_db
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{design_id}", response_model=DesignResponse)
async def get_design(
    design_id: int,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get a specific design."""
    design = await Design.get_or_none(id=design_id)
    
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
        
    if design.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this design")
        
    return design

@router.patch("/{design_id}", response_model=DesignResponse)
async def update_design(
    design_id: int,
    updates: DesignUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update a specific design."""
    design = await Design.get_or_none(id=design_id)
    
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
        
    if design.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this design")
        
    try:
        # Validate updates
        validation = await validation_service.validate_design({**design.model_data, **updates.dict()})
        if not validation["valid"]:
            raise ValidationError("Design validation failed", details=validation["issues"])
            
        # Update design
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(design, key, value)
            
        await design.save()
        
        # Schedule preview update
        background_tasks.add_task(
            _update_design_preview,
            design,
            {"resolution": "preview"}
        )
        
        return design
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{design_id}/validate", response_model=DesignValidationResponse)
async def validate_design(
    design_id: int,
    validation_request: DesignValidationRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Validate design changes before applying them."""
    design = await Design.get_or_none(id=design_id)
    
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
        
    if design.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to validate this design")
        
    try:
        # Combine current design with proposed changes
        design_data = {**design.model_data, **validation_request.changes}
        
        # Run validation
        validation_results = await validation_service.validate_design(design_data)
        
        return validation_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{design_id}")
async def delete_design(
    design_id: int,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Delete a specific design."""
    design = await Design.get_or_none(id=design_id)
    
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
        
    if design.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this design")
        
    await design.delete()
    
    return {"message": "Design deleted successfully"}

@router.get("/{design_id}/preview", response_model=Dict[str, Any])
async def get_design_preview(
    design_id: int,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get the latest preview for a design."""
    design = await Design.get_or_none(id=design_id)
    
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
        
    if design.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this design")
        
    if not design.preview_data:
        # Generate preview if it doesn't exist
        preview = await render_processor.process(
            design.model_data,
            {"resolution": "preview"}
        )
        design.preview_data = preview
        await design.save()
        
    return design.preview_data

async def _update_design_preview(design: Design, render_settings: Dict[str, Any]) -> None:
    """Background task to update design preview."""
    try:
        preview = await render_processor.process(
            design.model_data,
            render_settings
        )
        design.preview_data = preview
        await design.save()
        
    except Exception as e:
        # Log error but don't raise - this is a background task
        print(f"Error updating design preview: {str(e)}")  # Use proper logging in production
