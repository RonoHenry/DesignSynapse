from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.db.database import SessionLocal
from app.warehouse.etl import WarehouseETL
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def init_warehouse_scheduler():
    scheduler = BackgroundScheduler()
    
    def run_etl_job():
        """Run the ETL job with a new database session"""
        try:
            db = SessionLocal()
            etl = WarehouseETL(db)
            
            # Run the daily ETL process
            etl.run_daily_etl()
            
            # Populate date dimension for the next 365 days if needed
            today = datetime.now()
            etl.populate_date_dimension(
                start_date=today,
                end_date=today + timedelta(days=365)
            )
            
            logger.info("Warehouse ETL job completed successfully")
            
        except Exception as e:
            logger.error(f"Error in warehouse ETL job: {str(e)}")
        finally:
            db.close()
    
    # Schedule the ETL job to run daily at 1 AM
    scheduler.add_job(
        run_etl_job,
        trigger=CronTrigger(hour=1, minute=0),
        id='warehouse_etl_job',
        name='Daily Warehouse ETL',
        replace_existing=True
    )
    
    # Add a job to update fact tables every hour
    def update_facts_job():
        try:
            db = SessionLocal()
            etl = WarehouseETL(db)
            etl.update_project_metrics()
            logger.info("Fact tables updated successfully")
        except Exception as e:
            logger.error(f"Error updating fact tables: {str(e)}")
        finally:
            db.close()
    
    scheduler.add_job(
        update_facts_job,
        trigger=CronTrigger(minute=0),  # Run every hour at minute 0
        id='update_facts_job',
        name='Hourly Fact Table Updates',
        replace_existing=True
    )
    
    # Start the scheduler
    scheduler.start()
    logger.info("Warehouse scheduler initialized")
