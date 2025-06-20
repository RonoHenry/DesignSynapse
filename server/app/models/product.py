from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    project = relationship("Project", back_populates="products")
