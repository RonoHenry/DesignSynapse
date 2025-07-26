from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.warehouse.models import DimUser, DimProject, DimProduct, DimDate
from app.warehouse.models import FactProjectMetrics, FactProductUsage, FactProjectDaily
from app.models.user import User
from app.models.project import Project
from app.models.product import Product
from typing import List
import logging

logger = logging.getLogger(__name__)

class WarehouseETL:
    def __init__(self, db: Session):
        self.db = db

    def populate_date_dimension(self, start_date: datetime, end_date: datetime):
        """Populate the date dimension table with a range of dates"""
        current_date = start_date
        while current_date <= end_date:
            date_key = int(current_date.strftime('%Y%m%d'))
            
            # Check if date already exists
            if not self.db.query(DimDate).filter_by(date_key=date_key).first():
                dim_date = DimDate(
                    date_key=date_key,
                    date=current_date,
                    year=current_date.year,
                    quarter=(current_date.month - 1) // 3 + 1,
                    month=current_date.month,
                    month_name=current_date.strftime('%B'),
                    day=current_date.day,
                    day_of_week=current_date.weekday(),
                    day_name=current_date.strftime('%A'),
                    is_weekend=1 if current_date.weekday() >= 5 else 0,
                    is_holiday=0  # TODO: Implement holiday detection
                )
                self.db.add(dim_date)
            
            current_date += timedelta(days=1)
        
        self.db.commit()

    def update_user_dimension(self):
        """Update the user dimension with any changes"""
        users = self.db.query(User).all()
        for user in users:
            existing = self.db.query(DimUser).filter_by(
                user_id=user.id,
                is_current=1
            ).first()
            
            # If user exists and has changes, update it
            if existing and (
                existing.username != user.username or
                existing.email != user.email or
                existing.is_active != user.is_active
            ):
                # Set current record as inactive
                existing.is_current = 0
                existing.effective_to = datetime.now()
                
                # Create new current record
                new_dim_user = DimUser(
                    user_id=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                    created_date=user.created_at,
                    effective_from=datetime.now(),
                    is_current=1
                )
                self.db.add(new_dim_user)
            
            # If user doesn't exist, create it
            elif not existing:
                new_dim_user = DimUser(
                    user_id=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                    created_date=user.created_at,
                    effective_from=datetime.now(),
                    is_current=1
                )
                self.db.add(new_dim_user)
        
        self.db.commit()

    def update_project_metrics(self):
        """Update the project metrics fact table"""
        today_key = int(datetime.now().strftime('%Y%m%d'))
        
        projects = self.db.query(Project).all()
        for project in projects:
            # Get dimension keys
            dim_project = self.db.query(DimProject).filter_by(
                project_id=project.id,
                is_current=1
            ).first()
            
            dim_user = self.db.query(DimUser).filter_by(
                user_id=project.user_id,
                is_current=1
            ).first()
            
            if dim_project and dim_user:
                # Calculate metrics
                products = self.db.query(Product).filter_by(project_id=project.id).all()
                total_value = sum(p.price or 0 for p in products)
                
                metrics = FactProjectMetrics(
                    date_key=today_key,
                    project_key=dim_project.project_key,
                    user_key=dim_user.user_key,
                    total_products=len(products),
                    total_value=total_value,
                    # Other metrics would be calculated here
                )
                self.db.add(metrics)
        
        self.db.commit()

    def run_daily_etl(self):
        """Run the daily ETL process"""
        try:
            logger.info("Starting daily ETL process")
            
            # Update dimensions
            self.update_user_dimension()
            # Add other dimension updates here
            
            # Update facts
            self.update_project_metrics()
            # Add other fact updates here
            
            logger.info("Daily ETL process completed successfully")
            
        except Exception as e:
            logger.error(f"Error in daily ETL process: {str(e)}")
            self.db.rollback()
            raise
