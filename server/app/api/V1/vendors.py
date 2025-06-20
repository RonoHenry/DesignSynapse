from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud
from app.models.product import Product
from app.db.database import get_db
from typing import List
from fastapi import status

router = APIRouter()

@router.post("/products/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_product(name: str, description: str, category: str, price: float, project_id: int, db: Session = Depends(get_db)):
    product = crud.create_product(db, name, description, category, price, project_id)
    return {"id": product.id, "name": product.name}

@router.get("/products/{product_id}", response_model=dict)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product.id, "name": product.name, "description": product.description}

@router.get("/products/", response_model=List[dict])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.list_products(db, skip, limit)
    return [{"id": p.id, "name": p.name, "description": p.description} for p in products]

@router.put("/products/{product_id}", response_model=dict)
def update_product(product_id: int, name: str = None, description: str = None, category: str = None, price: float = None, db: Session = Depends(get_db)):
    product = crud.update_product(db, product_id, name=name, description=description, category=category, price=price)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product.id, "name": product.name, "description": product.description}

@router.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}
