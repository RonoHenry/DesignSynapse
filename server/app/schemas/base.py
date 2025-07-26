from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
