from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.models.project import Project
from app.models.product import Product
from app.db.database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_data():
    db = SessionLocal()
    try:
        # Create test user
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=pwd_context.hash("password123"),
            is_active=True
        )
        db.add(test_user)
        db.flush()  # Flush to get the user id

        # Create two projects
        project1 = Project(
            name="Modern House Design",
            description="A contemporary residential project with sustainable features",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=90),
            user_id=test_user.id
        )
        
        project2 = Project(
            name="Office Renovation",
            description="Commercial space renovation with modern amenities",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=45),
            user_id=test_user.id
        )
        
        db.add_all([project1, project2])
        db.flush()  # Flush to get project ids

        # Create products for each project
        products = [
            Product(
                name="Solar Panels",
                description="High-efficiency solar panels for roof installation",
                category="Renewable Energy",
                price=5000.00,
                project_id=project1.id
            ),
            Product(
                name="Smart Lighting System",
                description="IoT-based LED lighting system",
                category="Electronics",
                price=2500.00,
                project_id=project1.id
            ),
            Product(
                name="Office Desks",
                description="Modern ergonomic workstations",
                category="Furniture",
                price=800.00,
                project_id=project2.id
            ),
            Product(
                name="Conference Room Setup",
                description="Complete audio-visual solution for meetings",
                category="Electronics",
                price=3500.00,
                project_id=project2.id
            )
        ]
        
        db.add_all(products)
        db.commit()
        
        print("Sample data inserted successfully!")
        
        # Print the data to verify
        print("\nCreated User:")
        print(f"Username: {test_user.username}, Email: {test_user.email}")
        
        print("\nCreated Projects:")
        for project in [project1, project2]:
            print(f"\nProject: {project.name}")
            print(f"Description: {project.description}")
            print("Products:")
            for product in db.query(Product).filter_by(project_id=project.id).all():
                print(f"- {product.name} (${product.price})")

    except Exception as e:
        print(f"Error inserting sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
