from pydantic import BaseModel, constr, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal
from .base import TimestampMixin

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None

class ProductCreate(ProductBase):
    project_id: int

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    project_id: Optional[int] = None

class ProductInDB(ProductBase, TimestampMixin):
    id: int
    project_id: int
    
    class Config:
        from_attributes = True

class ProductResponse(ProductInDB):
    pass
