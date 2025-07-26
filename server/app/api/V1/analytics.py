from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.warehouse.analytics import WarehouseAnalytics
from datetime import datetime, timedelta
from typing import List, Dict, Any

router = APIRouter()

@router.get("/analytics/project-performance")
def get_project_performance(
    days: int = 30,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get project performance metrics for the last N days"""
    analytics = WarehouseAnalytics(db)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return analytics.get_project_performance(start_date, end_date)

@router.get("/analytics/top-products")
def get_top_products(
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get top products by usage and value"""
    analytics = WarehouseAnalytics(db)
    return analytics.get_top_products(limit)

@router.get("/analytics/user-activity")
def get_user_activity(
    days: int = 30,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get user activity metrics"""
    analytics = WarehouseAnalytics(db)
    return analytics.get_user_activity(days)

@router.get("/analytics/project/{project_id}/trends")
def get_project_trends(
    project_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get detailed trends for a specific project"""
    analytics = WarehouseAnalytics(db)
    return analytics.get_project_trends(project_id, days)

# Example query usage:
"""
# Get project performance for last 30 days
GET /analytics/project-performance?days=30

# Get top 5 products
GET /analytics/top-products?limit=5

# Get user activity for last week
GET /analytics/user-activity?days=7

# Get trends for project with ID 1
GET /analytics/project/1/trends?days=30
"""
