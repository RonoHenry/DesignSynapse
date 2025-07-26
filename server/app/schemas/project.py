from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime
from .base import TimestampMixin

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None

class ProjectInDB(ProjectBase, TimestampMixin):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class ProjectResponse(ProjectInDB):
    products: List['ProductResponse'] = []

class ProjectWithDetails(ProjectResponse):
    user: 'UserResponse'
