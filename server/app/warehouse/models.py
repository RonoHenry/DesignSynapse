"""SQLAlchemy models for data warehouse tables."""
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, Float, ForeignKey
from app.db.database import Base

class DimDate(Base):
    """Dimension table for dates."""
    __tablename__ = 'dim_date'

    date_key = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    month_name = Column(String, nullable=False)
    day = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    day_name = Column(String, nullable=False)
    is_weekend = Column(Boolean, nullable=False)
    is_holiday = Column(Boolean, nullable=False)


class DimUser(Base):
    """Dimension table for users."""
    __tablename__ = 'dim_users'

    user_key = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_current = Column(Boolean, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=True)


class DimProject(Base):
    """Dimension table for projects."""
    __tablename__ = 'dim_projects'

    project_key = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    type = Column(String, nullable=False)
    is_current = Column(Boolean, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=True)


class DimProduct(Base):
    """Dimension table for products."""
    __tablename__ = 'dim_products'

    product_key = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    vendor = Column(String, nullable=False)
    is_current = Column(Boolean, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=True)


class FactProjectMetrics(Base):
    """Fact table for project metrics."""
    __tablename__ = 'fact_project_metrics'

    id = Column(Integer, primary_key=True)
    date_key = Column(Integer, ForeignKey('dim_date.date_key'), nullable=False)
    project_key = Column(Integer, ForeignKey('dim_projects.project_key'), nullable=False)
    user_key = Column(Integer, ForeignKey('dim_users.user_key'), nullable=False)
    total_products = Column(Integer, nullable=False)
    total_value = Column(Numeric(10, 2), nullable=False)
    completion_percentage = Column(Float, nullable=False)


class FactProductUsage(Base):
    """Fact table for product usage."""
    __tablename__ = 'fact_product_usage'

    id = Column(Integer, primary_key=True)
    date_key = Column(Integer, ForeignKey('dim_date.date_key'), nullable=False)
    product_key = Column(Integer, ForeignKey('dim_products.product_key'), nullable=False)
    project_key = Column(Integer, ForeignKey('dim_projects.project_key'), nullable=False)
    quantity_used = Column(Integer, nullable=False)
    total_cost = Column(Numeric(10, 2), nullable=False)
    efficiency_score = Column(Float, nullable=False)


class FactProjectDaily(Base):
    """Fact table for daily project metrics."""
    __tablename__ = 'fact_project_daily'

    id = Column(Integer, primary_key=True)
    date_key = Column(Integer, ForeignKey('dim_date.date_key'), nullable=False)
    project_key = Column(Integer, ForeignKey('dim_projects.project_key'), nullable=False)
    total_value = Column(Numeric(10, 2), nullable=False)
    tasks_completed = Column(Integer, nullable=False)
