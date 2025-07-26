import os
import shutil
from datetime import datetime
import subprocess
import logging
from pathlib import Path

class DatabaseBackup:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            filename=self.backup_dir / "backup.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def create_backup(self, db_path: str = "./test.db") -> bool:
        """Create a backup of the SQLite database"""
        try:
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}.db"
            
            # Ensure source database exists
            if not os.path.exists(db_path):
                self.logger.error(f"Database file not found: {db_path}")
                return False
            
            # Create backup using SQLite's backup API
            self._sqlite_backup(db_path, str(backup_path))
            
            # Verify backup
            if not os.path.exists(backup_path):
                self.logger.error("Backup file was not created")
                return False
                
            self.logger.info(f"Backup created successfully: {backup_path}")
            
            # Cleanup old backups
            self._cleanup_old_backups()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}")
            return False

    def _sqlite_backup(self, source: str, destination: str):
        """Create a backup using SQLite's backup command"""
        command = f'sqlite3 "{source}" ".backup \'{destination}\'"'
        subprocess.run(command, shell=True, check=True)

    def restore_backup(self, backup_path: str, target_path: str = "./test.db") -> bool:
        """Restore database from backup"""
        try:
            # Ensure backup exists
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Create backup of current database before restore
            if os.path.exists(target_path):
                self.create_backup(target_path)
            
            # Restore using SQLite
            command = f'sqlite3 "{backup_path}" ".backup \'{target_path}\'"'
            subprocess.run(command, shell=True, check=True)
            
            self.logger.info(f"Database restored successfully from {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}")
            return False

    def _cleanup_old_backups(self, keep_days: int = 7):
        """Remove backups older than specified days"""
        try:
            current_time = datetime.now()
            for backup_file in self.backup_dir.glob("backup_*.db"):
                file_age = datetime.fromtimestamp(os.path.getctime(backup_file))
                if (current_time - file_age).days > keep_days:
                    os.remove(backup_file)
                    self.logger.info(f"Removed old backup: {backup_file}")
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")

# Usage example
backup_manager = DatabaseBackup()
