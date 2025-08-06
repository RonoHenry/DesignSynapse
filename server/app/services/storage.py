"""Design storage and versioning service."""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import hashlib
from pathlib import Path
import asyncio
import aiofiles
import shutil
from ..core.errors import StorageError

class DesignStorage:
    """Service for managing design storage and versioning."""

    def __init__(self, base_path: str, max_versions: int = 10):
        """Initialize storage service.
        
        Args:
            base_path: Base directory for storing designs
            max_versions: Maximum number of versions to keep per design
        """
        self.base_path = Path(base_path)
        self.max_versions = max_versions
        self._ensure_storage_dirs()
        
    def _ensure_storage_dirs(self) -> None:
        """Ensure required storage directories exist."""
        (self.base_path / "designs").mkdir(parents=True, exist_ok=True)
        (self.base_path / "versions").mkdir(parents=True, exist_ok=True)
        (self.base_path / "exports").mkdir(parents=True, exist_ok=True)
        
    async def store_design(
        self,
        design_id: int,
        design_data: Dict[str, Any],
        version_note: Optional[str] = None
    ) -> Dict[str, Any]:
        """Store a new version of a design.
        
        Args:
            design_id: Unique identifier for the design
            design_data: Design data to store
            version_note: Optional note for this version
            
        Returns:
            Dict containing version information
        """
        try:
            # Generate version hash
            version_hash = self._generate_version_hash(design_data)
            timestamp = datetime.utcnow()
            
            # Create version metadata
            version_info = {
                "version_hash": version_hash,
                "timestamp": timestamp.isoformat(),
                "version_note": version_note,
                "design_id": design_id
            }
            
            # Store design data
            design_path = self._get_design_path(design_id)
            version_path = self._get_version_path(design_id, version_hash)
            
            async with aiofiles.open(version_path, 'w') as f:
                await f.write(json.dumps(design_data))
                
            # Update version history
            history = await self._update_version_history(design_id, version_info)
            
            # Create symlink to latest version
            latest_path = design_path / "latest"
            if latest_path.exists():
                latest_path.unlink()
            latest_path.symlink_to(version_path)
            
            return {
                "version_hash": version_hash,
                "timestamp": timestamp,
                "version_note": version_note,
                "history": history
            }
            
        except Exception as e:
            raise StorageError(f"Failed to store design: {str(e)}")
            
    async def get_design(
        self,
        design_id: int,
        version_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        """Retrieve a specific version of a design.
        
        Args:
            design_id: Design identifier
            version_hash: Optional specific version hash
            
        Returns:
            Design data for requested version
        """
        try:
            if version_hash:
                version_path = self._get_version_path(design_id, version_hash)
            else:
                # Get latest version
                design_path = self._get_design_path(design_id)
                version_path = design_path / "latest"
                
            if not version_path.exists():
                raise StorageError("Design version not found")
                
            async with aiofiles.open(version_path, 'r') as f:
                content = await f.read()
                return json.loads(content)
                
        except Exception as e:
            raise StorageError(f"Failed to retrieve design: {str(e)}")
            
    async def get_version_history(self, design_id: int) -> List[Dict[str, Any]]:
        """Get version history for a design.
        
        Args:
            design_id: Design identifier
            
        Returns:
            List of version information dictionaries
        """
        try:
            history_path = self._get_design_path(design_id) / "history.json"
            if not history_path.exists():
                return []
                
            async with aiofiles.open(history_path, 'r') as f:
                content = await f.read()
                return json.loads(content)
                
        except Exception as e:
            raise StorageError(f"Failed to retrieve version history: {str(e)}")
            
    async def compare_versions(
        self,
        design_id: int,
        version1: str,
        version2: str
    ) -> Dict[str, Any]:
        """Compare two versions of a design.
        
        Args:
            design_id: Design identifier
            version1: First version hash
            version2: Second version hash
            
        Returns:
            Dictionary containing differences between versions
        """
        try:
            # Load both versions
            design1 = await self.get_design(design_id, version1)
            design2 = await self.get_design(design_id, version2)
            
            # Compare and generate diff
            return self._generate_design_diff(design1, design2)
            
        except Exception as e:
            raise StorageError(f"Failed to compare versions: {str(e)}")
            
    async def revert_to_version(
        self,
        design_id: int,
        version_hash: str
    ) -> Dict[str, Any]:
        """Revert a design to a specific version.
        
        Args:
            design_id: Design identifier
            version_hash: Version to revert to
            
        Returns:
            New version information
        """
        try:
            # Get old version
            old_design = await self.get_design(design_id, version_hash)
            
            # Store as new version with note
            return await self.store_design(
                design_id,
                old_design,
                f"Reverted to version {version_hash}"
            )
            
        except Exception as e:
            raise StorageError(f"Failed to revert version: {str(e)}")
            
    def _generate_version_hash(self, design_data: Dict[str, Any]) -> str:
        """Generate a unique hash for a design version."""
        content = json.dumps(design_data, sort_keys=True).encode()
        return hashlib.sha256(content).hexdigest()[:12]
        
    def _get_design_path(self, design_id: int) -> Path:
        """Get path for design storage."""
        path = self.base_path / "designs" / str(design_id)
        path.mkdir(parents=True, exist_ok=True)
        return path
        
    def _get_version_path(self, design_id: int, version_hash: str) -> Path:
        """Get path for specific version storage."""
        return self.base_path / "versions" / str(design_id) / f"{version_hash}.json"
        
    async def _update_version_history(
        self,
        design_id: int,
        version_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Update version history for a design."""
        history_path = self._get_design_path(design_id) / "history.json"
        
        try:
            if history_path.exists():
                async with aiofiles.open(history_path, 'r') as f:
                    content = await f.read()
                    history = json.loads(content)
            else:
                history = []
                
            # Add new version
            history.insert(0, version_info)
            
            # Trim to max versions
            if len(history) > self.max_versions:
                # Remove old version files
                for version in history[self.max_versions:]:
                    old_version_path = self._get_version_path(
                        design_id,
                        version["version_hash"]
                    )
                    if old_version_path.exists():
                        old_version_path.unlink()
                        
                history = history[:self.max_versions]
                
            # Save updated history
            async with aiofiles.open(history_path, 'w') as f:
                await f.write(json.dumps(history))
                
            return history
            
        except Exception as e:
            raise StorageError(f"Failed to update version history: {str(e)}")
            
    def _generate_design_diff(
        self,
        design1: Dict[str, Any],
        design2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate difference report between two design versions."""
        diff = {
            "added": {},
            "removed": {},
            "modified": {}
        }
        
        # Compare all keys
        all_keys = set(design1.keys()) | set(design2.keys())
        
        for key in all_keys:
            if key not in design1:
                diff["added"][key] = design2[key]
            elif key not in design2:
                diff["removed"][key] = design1[key]
            elif design1[key] != design2[key]:
                diff["modified"][key] = {
                    "from": design1[key],
                    "to": design2[key]
                }
                
        return diff
