from pydantic import BaseModel, constr, condecimal
from typing import Optional, List
from datetime import datetime
from .base import TimestampMixin

class ProjectBase(BaseModel):
    name: constr(min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[constr(min_length=1, max_length=255)] = None

class Project(ProjectBase, TimestampMixin):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: constr(min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    price: condecimal(decimal_places=2, ge=0)

class ProductCreate(ProductBase):
    project_id: int

class ProductUpdate(ProductBase):
    name: Optional[constr(min_length=1, max_length=255)] = None
    price: Optional[condecimal(decimal_places=2, ge=0)] = None

class Product(ProductBase, TimestampMixin):
    id: int
    project_id: int
    
    class Config:
        orm_mode = True
