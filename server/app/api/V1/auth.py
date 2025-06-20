from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud
from app.models.user import User
from app.db.database import get_db
from typing import List
from fastapi import status

router = APIRouter()

@router.post("/users/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(username: str, email: str, hashed_password: str, db: Session = Depends(get_db)):
    user = crud.create_user(db, username, email, hashed_password)
    return {"id": user.id, "username": user.username}

@router.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}

@router.get("/users/", response_model=List[dict])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.list_users(db, skip, limit)
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

@router.put("/users/{user_id}", response_model=dict)
def update_user(user_id: int, username: str = None, email: str = None, hashed_password: str = None, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, username=username, email=email, hashed_password=hashed_password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}
