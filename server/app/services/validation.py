"""Design validation service for DesignSynapse."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, validator
import numpy as np
from ..core.errors import ValidationError

class DesignMetrics(BaseModel):
    """Design metrics model for validation."""
    area: float = Field(..., gt=0)
    room_count: int = Field(..., gt=0)
    window_count: int = Field(..., ge=0)
    door_count: int = Field(..., gt=0)
    ceiling_height: float = Field(..., gt=0)
    total_wall_area: float = Field(..., gt=0)
    window_wall_ratio: float = Field(..., ge=0, le=1)

class DesignValidation(BaseModel):
    """Design validation parameters."""
    min_room_area: float = Field(default=80.0)  # sq ft
    min_window_wall_ratio: float = Field(default=0.1)
    max_window_wall_ratio: float = Field(default=0.4)
    min_door_width: float = Field(default=2.5)  # ft
    min_ceiling_height: float = Field(default=8.0)  # ft
    min_room_dimension: float = Field(default=6.0)  # ft
    max_wall_span: float = Field(default=30.0)  # ft

class ValidationService:
    """Service for validating architectural designs."""

    def __init__(self, validation_params: Optional[Dict[str, Any]] = None):
        """Initialize validation service with optional custom parameters."""
        self.params = DesignValidation(**(validation_params or {}))

    async def validate_design(self, design_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a design against architectural and safety requirements.
        
        Args:
            design_data: Dictionary containing design specifications
            
        Returns:
            Dictionary containing validation results and any issues found
        """
        try:
            # Extract metrics
            metrics = self._calculate_metrics(design_data)
            
            # Run validations
            validations = [
                self._validate_room_sizes(design_data),
                self._validate_window_requirements(metrics),
                self._validate_door_requirements(design_data),
                self._validate_structural_requirements(design_data)
            ]
            
            # Combine validation results
            issues = []
            for validation in validations:
                issues.extend(validation.get("issues", []))
            
            return {
                "valid": len(issues) == 0,
                "metrics": metrics.dict(),
                "issues": issues,
                "recommendations": self._generate_recommendations(metrics, issues)
            }
            
        except Exception as e:
            raise ValidationError(f"Design validation failed: {str(e)}")

    def _calculate_metrics(self, design_data: Dict[str, Any]) -> DesignMetrics:
        """Calculate key metrics from design data."""
        rooms = design_data.get("rooms", [])
        walls = design_data.get("walls", [])
        windows = design_data.get("windows", [])
        doors = design_data.get("doors", [])

        # Calculate areas
        total_area = sum(room.get("area", 0) for room in rooms)
        total_wall_area = sum(wall.get("area", 0) for wall in walls)
        total_window_area = sum(window.get("area", 0) for window in windows)

        return DesignMetrics(
            area=total_area,
            room_count=len(rooms),
            window_count=len(windows),
            door_count=len(doors),
            ceiling_height=design_data.get("ceiling_height", 0),
            total_wall_area=total_wall_area,
            window_wall_ratio=total_window_area / total_wall_area if total_wall_area > 0 else 0
        )

    def _validate_room_sizes(self, design_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate room dimensions and areas."""
        issues = []
        rooms = design_data.get("rooms", [])

        for i, room in enumerate(rooms):
            area = room.get("area", 0)
            dimensions = room.get("dimensions", {})
            width = dimensions.get("width", 0)
            length = dimensions.get("length", 0)

            if area < self.params.min_room_area:
                issues.append({
                    "type": "room_area",
                    "severity": "error",
                    "room": i + 1,
                    "message": f"Room {i + 1} area ({area:.1f} sq ft) is below minimum ({self.params.min_room_area} sq ft)"
                })

            if width < self.params.min_room_dimension:
                issues.append({
                    "type": "room_width",
                    "severity": "error",
                    "room": i + 1,
                    "message": f"Room {i + 1} width ({width:.1f} ft) is below minimum ({self.params.min_room_dimension} ft)"
                })

            if length < self.params.min_room_dimension:
                issues.append({
                    "type": "room_length",
                    "severity": "error",
                    "room": i + 1,
                    "message": f"Room {i + 1} length ({length:.1f} ft) is below minimum ({self.params.min_room_dimension} ft)"
                })

        return {"issues": issues}

    def _validate_window_requirements(self, metrics: DesignMetrics) -> Dict[str, Any]:
        """Validate window requirements for light and ventilation."""
        issues = []

        if metrics.window_wall_ratio < self.params.min_window_wall_ratio:
            issues.append({
                "type": "window_ratio",
                "severity": "error",
                "message": f"Window-to-wall ratio ({metrics.window_wall_ratio:.1%}) is below minimum ({self.params.min_window_wall_ratio:.1%})"
            })

        if metrics.window_wall_ratio > self.params.max_window_wall_ratio:
            issues.append({
                "type": "window_ratio",
                "severity": "warning",
                "message": f"Window-to-wall ratio ({metrics.window_wall_ratio:.1%}) exceeds recommended maximum ({self.params.max_window_wall_ratio:.1%})"
            })

        return {"issues": issues}

    def _validate_door_requirements(self, design_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate door dimensions and placement."""
        issues = []
        doors = design_data.get("doors", [])

        for i, door in enumerate(doors):
            width = door.get("width", 0)
            if width < self.params.min_door_width:
                issues.append({
                    "type": "door_width",
                    "severity": "error",
                    "door": i + 1,
                    "message": f"Door {i + 1} width ({width:.1f} ft) is below minimum ({self.params.min_door_width} ft)"
                })

        return {"issues": issues}

    def _validate_structural_requirements(self, design_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate structural requirements and limitations."""
        issues = []
        walls = design_data.get("walls", [])

        for i, wall in enumerate(walls):
            length = wall.get("length", 0)
            if length > self.params.max_wall_span:
                issues.append({
                    "type": "wall_span",
                    "severity": "warning",
                    "wall": i + 1,
                    "message": f"Wall {i + 1} span ({length:.1f} ft) exceeds recommended maximum ({self.params.max_wall_span} ft)"
                })

        return {"issues": issues}

    def _generate_recommendations(
        self,
        metrics: DesignMetrics,
        issues: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate design improvement recommendations based on validation results."""
        recommendations = []

        # Window recommendations
        if metrics.window_wall_ratio < self.params.min_window_wall_ratio:
            recommendations.append({
                "type": "windows",
                "priority": "high",
                "message": "Consider adding more windows to improve natural lighting and ventilation",
                "details": {
                    "current_ratio": metrics.window_wall_ratio,
                    "target_ratio": self.params.min_window_wall_ratio,
                    "additional_area_needed": (
                        self.params.min_window_wall_ratio - metrics.window_wall_ratio
                    ) * metrics.total_wall_area
                }
            })

        # Room size recommendations
        room_issues = [i for i in issues if i["type"].startswith("room_")]
        if room_issues:
            recommendations.append({
                "type": "room_size",
                "priority": "high",
                "message": "Adjust room dimensions to meet minimum size requirements",
                "details": {
                    "affected_rooms": [i["room"] for i in room_issues],
                    "min_area": self.params.min_room_area,
                    "min_dimension": self.params.min_room_dimension
                }
            })

        # Structural recommendations
        wall_issues = [i for i in issues if i["type"] == "wall_span"]
        if wall_issues:
            recommendations.append({
                "type": "structural",
                "priority": "medium",
                "message": "Consider adding structural supports for long wall spans",
                "details": {
                    "affected_walls": [i["wall"] for i in wall_issues],
                    "max_span": self.params.max_wall_span
                }
            })

        return recommendations
