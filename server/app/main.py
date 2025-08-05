from fastapi import FastAPI
from app.api.V1.projects import router as projects_router
from app.api.V1.vendors import router as products_router
from app.api.V1.auth import router as users_router
from app.services.ai.router import router as ai_router

app = FastAPI(
    title="DesignSynapse API",
    description="AI-driven platform for the DAEC industry",
    version="1.0.0"
)

# Core API routes
app.include_router(projects_router, prefix="/api/v1", tags=["Projects"])
app.include_router(products_router, prefix="/api/v1", tags=["Products"])
app.include_router(users_router, prefix="/api/v1", tags=["Users"])

# AI Services routes
app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI Services"])
