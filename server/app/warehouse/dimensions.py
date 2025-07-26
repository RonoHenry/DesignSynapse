from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class DimUser(Base):
    __tablename__ = "dim_users"
    
    user_key = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)  # Natural key from source
    username = Column(String(150))
    email = Column(String(255))
    is_active = Column(Integer)
    created_date = Column(DateTime)
    effective_from = Column(DateTime, server_default=func.now())
    effective_to = Column(DateTime, nullable=True)
    is_current = Column(Integer, default=1)

class DimProject(Base):
    __tablename__ = "dim_projects"
    
    project_key = Column(Integer, primary_key=True)
    project_id = Column(Integer, unique=True)  # Natural key from source
    name = Column(String(255))
    description = Column(String(1000))
    status = Column(String(50))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    effective_from = Column(DateTime, server_default=func.now())
    effective_to = Column(DateTime, nullable=True)
    is_current = Column(Integer, default=1)

class DimProduct(Base):
    __tablename__ = "dim_products"
    
    product_key = Column(Integer, primary_key=True)
    product_id = Column(Integer, unique=True)  # Natural key from source
    name = Column(String(255))
    category = Column(String(100))
    description = Column(String(1000))
    price_range = Column(String(50))  # Binned price ranges
    effective_from = Column(DateTime, server_default=func.now())
    effective_to = Column(DateTime, nullable=True)
    is_current = Column(Integer, default=1)

class DimDate(Base):
    __tablename__ = "dim_date"
    
    date_key = Column(Integer, primary_key=True)  # YYYYMMDD format
    date = Column(DateTime, unique=True)
    year = Column(Integer)
    quarter = Column(Integer)
    month = Column(Integer)
    month_name = Column(String(10))
    day = Column(Integer)
    day_of_week = Column(Integer)
    day_name = Column(String(10))
    is_weekend = Column(Integer)
    is_holiday = Column(Integer)
