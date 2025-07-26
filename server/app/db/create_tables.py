from app.db.database import Base, engine
# Import warehouse models to ensure they are registered with SQLAlchemy
from app.warehouse.models import (
    DimDate, DimUser, DimProject, DimProduct,
    FactProjectMetrics, FactProductUsage, FactProjectDaily
)

def create_all_tables():
    """Create all tables in the database."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all_tables()
