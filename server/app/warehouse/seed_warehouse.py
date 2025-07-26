from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.warehouse.models import (
    DimUser, DimProject, DimProduct, DimDate,
    FactProjectMetrics, FactProductUsage, FactProjectDaily
)
from app.warehouse.etl import WarehouseETL
from app.db.database import SessionLocal

def seed_warehouse_data():
    """Seed the data warehouse with initial test data"""
    db = SessionLocal()
    try:
        print("Starting data warehouse seeding...")
        
        # Initialize ETL
        etl = WarehouseETL(db)
        
        # 1. Populate Date Dimension for the next year
        print("Populating date dimension...")
        start_date = datetime.now()
        end_date = start_date + timedelta(days=365)
        etl.populate_date_dimension(start_date, end_date)
        
        # 2. Create sample dimension data
        print("Creating dimension records...")
        
        # Users dimension
        dim_user1 = DimUser(
            user_id=1,
            username="testuser",
            email="test@example.com",
            role="user",
            is_current=True,
            valid_from=datetime.now()
        )
        db.add(dim_user1)
        
        # Projects dimension
        projects = [
            DimProject(
                project_id=1,
                name="Modern House Design",
                status="In Progress",
                type="Residential",
                is_current=True,
                valid_from=datetime.now()
            ),
            DimProject(
                project_id=2,
                name="Office Renovation",
                status="Planning",
                type="Commercial",
                is_current=True,
                valid_from=datetime.now()
            )
        ]
        db.add_all(projects)
        
        # Products dimension
        products = [
            DimProduct(
                product_id=1,
                name="Solar Panels",
                category="Renewable Energy",
                vendor="SolarTech",
                is_current=True,
                valid_from=datetime.now()
            ),
            DimProduct(
                product_id=2,
                name="Smart Lighting System",
                category="Electronics",
                vendor="SmartLED",
                is_current=True,
                valid_from=datetime.now()
            )
        ]
        db.add_all(products)
        
        # Commit dimension data
        db.commit()
        
        # 3. Create sample fact data
        print("Creating fact records...")
        
        # Get dimension keys
        date_key = int(datetime.now().strftime('%Y%m%d'))
        
        # Project metrics facts
        metrics = [
            FactProjectMetrics(
                date_key=date_key,
                project_key=1,
                user_key=1,
                total_products=5,
                total_value=15000.00,
                completion_percentage=35.0
            ),
            FactProjectMetrics(
                date_key=date_key,
                project_key=2,
                user_key=1,
                total_products=3,
                total_value=8000.00,
                completion_percentage=20.0
            )
        ]
        db.add_all(metrics)
        
        # Product usage facts
        usages = [
            FactProductUsage(
                date_key=date_key,
                product_key=1,
                project_key=1,
                quantity_used=10,
                total_cost=7500.00,
                efficiency_score=92.5
            ),
            FactProductUsage(
                date_key=date_key,
                product_key=2,
                project_key=1,
                quantity_used=15,
                total_cost=3500.00,
                efficiency_score=88.0
            )
        ]
        db.add_all(usages)
        
        # Project daily facts
        daily_facts = [
            FactProjectDaily(
                date_key=date_key,
                project_key=1,
                total_value=15000.00,
                tasks_completed=3
            ),
            FactProjectDaily(
                date_key=date_key,
                project_key=2,
                total_value=8000.00,
                tasks_completed=1
            )
        ]
        db.add_all(daily_facts)
        
        # Commit fact data
        db.commit()
        print("Data warehouse seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding data warehouse: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_warehouse_data()
