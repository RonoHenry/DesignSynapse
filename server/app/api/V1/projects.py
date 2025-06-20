from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud
from app.models.project import Project
from app.db.database import Base
from typing import List

from fastapi import status

# Dependency to get DB session
from app.db.database import get_db

router = APIRouter()

@router.post("/projects/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_project(name: str, description: str, user_id: int, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    project = crud.create_project(db, name, description, user_id, start_date, end_date)
    return {"id": project.id, "name": project.name}

@router.get("/projects/{project_id}", response_model=dict)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"id": project.id, "name": project.name, "description": project.description}

@router.get("/projects/", response_model=List[dict])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.list_projects(db, skip, limit)
    return [{"id": p.id, "name": p.name, "description": p.description} for p in projects]

@router.put("/projects/{project_id}", response_model=dict)
def update_project(project_id: int, name: str = None, description: str = None, db: Session = Depends(get_db)):
    project = crud.update_project(db, project_id, name=name, description=description)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"id": project.id, "name": project.name, "description": project.description}

@router.delete("/projects/{project_id}", response_model=dict)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    success = crud.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"ok": True}
