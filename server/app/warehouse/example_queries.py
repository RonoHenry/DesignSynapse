from sqlalchemy import text
from app.db.database import SessionLocal
from datetime import datetime, timedelta

def run_example_queries():
    """Run example analytics queries against the data warehouse"""
    db = SessionLocal()
    try:
        # Example 1: Project Performance Overview
        print("\n=== Project Performance Overview ===")
        query1 = text("""
            SELECT 
                dp.name as project_name,
                SUM(fpm.total_products) as total_products,
                SUM(fpm.total_value) as total_value,
                AVG(fpm.completion_percentage) as avg_completion
            FROM dim_projects dp
            JOIN fact_project_metrics fpm ON dp.project_key = fpm.project_key
            WHERE dp.is_current = 1
            GROUP BY dp.project_key, dp.name
            ORDER BY total_value DESC
            LIMIT 5
        """)
        results1 = db.execute(query1)
        for row in results1:
            print(f"Project: {row.project_name}")
            print(f"Total Products: {row.total_products}")
            print(f"Total Value: ${row.total_value:,.2f}")
            print(f"Average Completion: {row.avg_completion:.1f}%\n")

        # Example 2: Product Usage Analysis
        print("\n=== Product Usage Analysis ===")
        query2 = text("""
            SELECT 
                dp.name as product_name,
                dp.category,
                SUM(fpu.quantity_used) as total_usage,
                SUM(fpu.total_cost) as total_cost,
                AVG(fpu.efficiency_score) as avg_efficiency
            FROM dim_products dp
            JOIN fact_product_usage fpu ON dp.product_key = fpu.product_key
            WHERE dp.is_current = 1
            GROUP BY dp.product_key, dp.name, dp.category
            ORDER BY total_cost DESC
            LIMIT 5
        """)
        results2 = db.execute(query2)
        for row in results2:
            print(f"Product: {row.product_name} ({row.category})")
            print(f"Total Usage: {row.total_usage}")
            print(f"Total Cost: ${row.total_cost:,.2f}")
            print(f"Efficiency Score: {row.avg_efficiency:.1f}\n")

        # Example 3: User Activity Metrics
        print("\n=== User Activity Metrics ===")
        query3 = text("""
            SELECT 
                du.username,
                COUNT(DISTINCT fpm.project_key) as projects_managed,
                SUM(fpm.total_value) as total_value_managed
            FROM dim_users du
            JOIN fact_project_metrics fpm ON du.user_key = fpm.user_key
            WHERE du.is_current = 1
            GROUP BY du.user_key, du.username
            ORDER BY total_value_managed DESC
            LIMIT 5
        """)
        results3 = db.execute(query3)
        for row in results3:
            print(f"User: {row.username}")
            print(f"Projects Managed: {row.projects_managed}")
            print(f"Total Value Managed: ${row.total_value_managed:,.2f}\n")

        # Example 4: Time-based Analysis
        print("\n=== Weekly Project Trends ===")
        query4 = text("""
            SELECT 
                dd.year,
                dd.month_name,
                COUNT(DISTINCT fpd.project_key) as active_projects,
                SUM(fpd.total_value) as total_value,
                AVG(fpd.tasks_completed) as avg_tasks_completed
            FROM dim_date dd
            JOIN fact_project_daily fpd ON dd.date_key = fpd.date_key
            GROUP BY dd.year, dd.month, dd.month_name
            ORDER BY dd.year, dd.month DESC
            LIMIT 6
        """)
        results4 = db.execute(query4)
        for row in results4:
            print(f"Period: {row.month_name} {row.year}")
            print(f"Active Projects: {row.active_projects}")
            print(f"Total Value: ${row.total_value:,.2f}")
            print(f"Avg Tasks Completed: {row.avg_tasks_completed:.1f}\n")

    finally:
        db.close()

if __name__ == "__main__":
    run_example_queries()
