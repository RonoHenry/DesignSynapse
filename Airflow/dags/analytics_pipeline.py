"""
Analytics Pipeline DAG to automate warehouse analytics tasks.
This DAG runs analytics tasks every 4 hours to keep metrics updated.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import logging

# Add server directory to Python path
sys.path.append('D:/Projects/DesignSynapse/server')

from app.warehouse.analytics import WarehouseAnalytics
from app.db.database import SessionLocal

logger = logging.getLogger(__name__)

def run_analytics_task(task_type: str, **kwargs) -> dict:
    """
    Generic function to run analytics tasks
    Args:
        task_type: Type of analytics task to run
        **kwargs: Additional arguments for specific tasks
    """
    logger.info(f"Running {task_type} analytics task")
    db = SessionLocal()
    try:
        analytics = WarehouseAnalytics(db)
        result = None
        
        if task_type == 'project_performance':
            end_date = datetime.now()
            start_date = end_date - timedelta(days=kwargs.get('days', 30))
            result = analytics.get_project_performance(start_date, end_date)
        elif task_type == 'top_products':
            result = analytics.get_top_products(limit=kwargs.get('limit', 10))
        elif task_type == 'user_activity':
            result = analytics.get_user_activity(days=kwargs.get('days', 30))
        elif task_type == 'project_trends':
            result = analytics.get_project_trends(
                project_id=kwargs.get('project_id'),
                days=kwargs.get('days', 30)
            )
        
        logger.info(f"Successfully completed {task_type} analytics task")
        return result
    except Exception as e:
        logger.error(f"Error in {task_type} analytics task: {str(e)}")
        raise
    finally:
        db.close()

# DAG definition
default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 7, 29),
    'email_on_failure': True,
    'email_on_retry': True,
}

with DAG(
    'analytics_pipeline',
    default_args=default_args,
    description='Analytics data pipeline',
    schedule_interval='0 */4 * * *',  # Every 4 hours
    catchup=False,
    tags=['analytics', 'warehouse']
) as dag:

    # Project Performance Task
    project_performance = PythonOperator(
        task_id='project_performance',
        python_callable=run_analytics_task,
        op_kwargs={'task_type': 'project_performance', 'days': 30}
    )

    # Top Products Task
    top_products = PythonOperator(
        task_id='top_products',
        python_callable=run_analytics_task,
        op_kwargs={'task_type': 'top_products', 'limit': 10}
    )

    # User Activity Task
    user_activity = PythonOperator(
        task_id='user_activity',
        python_callable=run_analytics_task,
        op_kwargs={'task_type': 'user_activity', 'days': 30}
    )

    # Project Trends Task (for all active projects)
    project_trends = PythonOperator(
        task_id='project_trends',
        python_callable=run_analytics_task,
        op_kwargs={'task_type': 'project_trends', 'days': 30}
    )

    # Set task dependencies
    project_performance >> top_products >> user_activity >> project_trends
