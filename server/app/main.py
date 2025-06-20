from fastapi import FastAPI
from app.api.V1.projects import router as projects_router
from app.api.V1.vendors import router as products_router
from app.api.V1.auth import router as users_router

app = FastAPI()

app.include_router(projects_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
