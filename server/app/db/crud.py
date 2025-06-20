from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.user import User
from app.models.product import Product
from typing import List, Optional

def create_project(db: Session, name: str, description: str, user_id: int, start_date=None, end_date=None) -> Project:
    project = Project(
        name=name,
        description=description,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_project(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()

def list_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    return db.query(Project).offset(skip).limit(limit).all()

def update_project(db: Session, project_id: int, **kwargs) -> Optional[Project]:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    for key, value in kwargs.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int) -> bool:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return False
    db.delete(project)
    db.commit()
    return True

# Product CRUD

def create_product(db: Session, name: str, description: str, category: str, price: float, project_id: int) -> Product:
    product = Product(
        name=name,
        description=description,
        category=category,
        price=price,
        project_id=project_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, **kwargs) -> Optional[Product]:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    for key, value in kwargs.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True

# User CRUD

def create_user(db: Session, username: str, email: str, hashed_password: str) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
