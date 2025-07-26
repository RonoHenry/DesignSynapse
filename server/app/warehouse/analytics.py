from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.warehouse.dimensions import DimUser, DimProject, DimProduct, DimDate
from app.warehouse.facts import FactProjectMetrics, FactProductUsage, FactProjectDaily

class WarehouseAnalytics:
    def __init__(self, db: Session):
        self.db = db

    def get_project_performance(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get project performance metrics over time"""
        return self.db.query(
            DimProject.name.label('project_name'),
            DimDate.date,
            func.sum(FactProjectMetrics.total_value).label('total_value'),
            func.sum(FactProjectMetrics.total_products).label('total_products'),
            func.avg(FactProjectMetrics.completion_percentage).label('avg_completion')
        ).join(
            FactProjectMetrics, DimProject.project_key == FactProjectMetrics.project_key
        ).join(
            DimDate, DimDate.date_key == FactProjectMetrics.date_key
        ).filter(
            and_(
                DimDate.date >= start_date,
                DimDate.date <= end_date,
                DimProject.is_current == 1
            )
        ).group_by(
            DimProject.name,
            DimDate.date
        ).order_by(
            DimDate.date
        ).all()

    def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top products by usage and value"""
        return self.db.query(
            DimProduct.name.label('product_name'),
            func.sum(FactProductUsage.quantity_used).label('total_usage'),
            func.sum(FactProductUsage.total_cost).label('total_cost'),
            func.avg(FactProductUsage.efficiency_score).label('avg_efficiency')
        ).join(
            FactProductUsage, DimProduct.product_key == FactProductUsage.product_key
        ).filter(
            DimProduct.is_current == 1
        ).group_by(
            DimProduct.name
        ).order_by(
            desc('total_usage')
        ).limit(limit).all()

    def get_user_activity(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get user activity metrics"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.db.query(
            DimUser.username,
            func.count(FactProjectMetrics.id).label('total_updates'),
            func.sum(FactProjectMetrics.total_value).label('total_value_managed')
        ).join(
            FactProjectMetrics, DimUser.user_key == FactProjectMetrics.user_key
        ).join(
            DimDate, DimDate.date_key == FactProjectMetrics.date_key
        ).filter(
            and_(
                DimDate.date >= cutoff_date,
                DimUser.is_current == 1
            )
        ).group_by(
            DimUser.username
        ).all()

    def get_project_trends(self, project_id: int, days: int = 30) -> Dict[str, Any]:
        """Get detailed trends for a specific project"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get project metrics over time
        metrics = self.db.query(
            DimDate.date,
            FactProjectDaily.products_count,
            FactProjectDaily.total_value,
            FactProjectDaily.tasks_completed,
            FactProjectDaily.tasks_pending,
            FactProjectDaily.budget_utilized
        ).join(
            DimProject, and_(
                DimProject.project_key == FactProjectDaily.project_key,
                DimProject.project_id == project_id,
                DimProject.is_current == 1
            )
        ).join(
            DimDate, DimDate.date_key == FactProjectDaily.date_key
        ).filter(
            DimDate.date >= cutoff_date
        ).order_by(
            DimDate.date
        ).all()
        
        # Calculate trends and metrics
        return {
            'daily_metrics': [dict(row) for row in metrics],
            'summary': {
                'avg_daily_progress': sum(m.tasks_completed for m in metrics) / len(metrics),
                'total_budget_utilized': sum(m.budget_utilized for m in metrics),
                'product_count_trend': [m.products_count for m in metrics],
                'completion_trend': [
                    m.tasks_completed / (m.tasks_completed + m.tasks_pending)
                    if (m.tasks_completed + m.tasks_pending) > 0 else 0
                    for m in metrics
                ]
            }
        }
