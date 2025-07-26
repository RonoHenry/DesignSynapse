from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class FactProjectMetrics(Base):
    __tablename__ = "fact_project_metrics"
    
    id = Column(Integer, primary_key=True)
    date_key = Column(Integer, ForeignKey("dim_date.date_key"), nullable=False)
    project_key = Column(Integer, ForeignKey("dim_projects.project_key"), nullable=False)
    user_key = Column(Integer, ForeignKey("dim_users.user_key"), nullable=False)
    
    # Metrics
    total_products = Column(Integer, default=0)
    total_value = Column(Numeric(12, 2), default=0)
    completion_percentage = Column(Numeric(5, 2), default=0)
    active_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    
    # Time stamp for when this fact was recorded
    created_at = Column(DateTime, server_default=func.now())

    # Create indexes for commonly queried columns
    __table_args__ = (
        Index('idx_project_metrics_date', date_key),
        Index('idx_project_metrics_project', project_key),
        Index('idx_project_metrics_user', user_key),
    )

class FactProductUsage(Base):
    __tablename__ = "fact_product_usage"
    
    id = Column(Integer, primary_key=True)
    date_key = Column(Integer, ForeignKey("dim_date.date_key"), nullable=False)
    product_key = Column(Integer, ForeignKey("dim_products.product_key"), nullable=False)
    project_key = Column(Integer, ForeignKey("dim_projects.project_key"), nullable=False)
    
    # Metrics
    quantity_used = Column(Integer, default=0)
    total_cost = Column(Numeric(12, 2), default=0)
    usage_hours = Column(Numeric(8, 2), default=0)
    efficiency_score = Column(Numeric(5, 2), default=0)
    
    # Time stamp for when this fact was recorded
    created_at = Column(DateTime, server_default=func.now())

    # Create indexes for commonly queried columns
    __table_args__ = (
        Index('idx_product_usage_date', date_key),
        Index('idx_product_usage_product', product_key),
        Index('idx_product_usage_project', project_key),
    )

# Fact table for daily snapshot of project status
class FactProjectDaily(Base):
    __tablename__ = "fact_project_daily"
    __table_args__ = (
        # Partition by date_key for better query performance
        {"postgresql_partition_by": "RANGE (date_key)"}
    )
    
    id = Column(Integer, primary_key=True)
    date_key = Column(Integer, ForeignKey("dim_date.date_key"), nullable=False)
    project_key = Column(Integer, ForeignKey("dim_projects.project_key"), nullable=False)
    user_key = Column(Integer, ForeignKey("dim_users.user_key"), nullable=False)
    
    # Daily metrics
    products_count = Column(Integer, default=0)
    total_value = Column(Numeric(12, 2), default=0)
    tasks_completed = Column(Integer, default=0)
    tasks_pending = Column(Integer, default=0)
    budget_utilized = Column(Numeric(12, 2), default=0)
    
    # Time stamp for when this snapshot was taken
    snapshot_time = Column(DateTime, server_default=func.now())

    # Create indexes for commonly queried columns
    __table_args__ = (
        Index('idx_project_daily_date', date_key),
        Index('idx_project_daily_project', project_key),
        Index('idx_project_daily_user', user_key),
    )
