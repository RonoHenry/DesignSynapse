"""Design-related schemas."""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class DesignBase(BaseModel):
    """Base schema for design data."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    style: str = Field(..., min_length=1, max_length=50)
    model_data: Dict[str, Any] = Field(...)
    metadata: Optional[Dict[str, Any]] = None

class DesignCreate(DesignBase):
    """Schema for creating a new design."""
    pass

class DesignUpdate(BaseModel):
    """Schema for updating a design."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    style: Optional[str] = Field(None, min_length=1, max_length=50)
    model_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class DesignResponse(DesignBase):
    """Schema for design responses."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    preview_data: Optional[Dict[str, Any]] = None
    
    class Config:
        orm_mode = True

class ValidationIssue(BaseModel):
    """Schema for validation issues."""
    type: str
    severity: str
    message: str
    details: Optional[Dict[str, Any]] = None

class Recommendation(BaseModel):
    """Schema for design recommendations."""
    type: str
    priority: str
    message: str
    details: Optional[Dict[str, Any]] = None

class DesignMetricsResponse(BaseModel):
    """Schema for design metrics."""
    area: float
    room_count: int
    window_count: int
    door_count: int
    ceiling_height: float
    total_wall_area: float
    window_wall_ratio: float

class DesignValidationRequest(BaseModel):
    """Schema for design validation requests."""
    changes: Dict[str, Any] = Field(...)

class DesignValidationResponse(BaseModel):
    """Schema for design validation responses."""
    valid: bool
    metrics: DesignMetricsResponse
    issues: List[ValidationIssue] = []
    recommendations: List[Recommendation] = []
