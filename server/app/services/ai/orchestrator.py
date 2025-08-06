"""AI Service Orchestrator for managing and coordinating AI services."""

from typing import Dict, Any, List
import logging
from pathlib import Path
import asyncio
from fastapi import BackgroundTasks

from app.services.ai.design.model import DesignGenerator
from app.services.ai.render.processor import RenderProcessor
from app.services.ai.engineering.calculator import EngineeringCalculator
from app.services.ai.cost.estimator import CostEstimator
from app.core.config import get_settings

logger = logging.getLogger(__name__)

class AIOrchestrator:
    def __init__(self):
        """Initialize AI service orchestrator."""
        self.design_generator = DesignGenerator()
        self.render_processor = RenderProcessor()
        self.engineering_calculator = EngineeringCalculator()
        self.cost_estimator = CostEstimator()
        
        # Service status tracking
        self.service_status = {
            "design_generator": "initialized",
            "render_processor": "initialized",
            "engineering_calculator": "initialized",
            "cost_estimator": "initialized"
        }
        
    async def generate_complete_design(
        self,
        requirements: Dict[str, Any],
        background_tasks: BackgroundTasks
    ) -> Dict[str, Any]:
        """Generate a complete design including floor plans, renderings, calculations and cost estimates.
        
        Args:
            requirements: Client requirements for the design
            background_tasks: FastAPI background tasks for async processing
            
        Returns:
            Dictionary containing all design outputs
        """
        try:
            # Step 1: Generate basic design
            design_output = await self._generate_design(requirements)
            
            # Step 2: Start parallel processing tasks
            render_task = asyncio.create_task(
                self._process_renderings(design_output["floor_plans"])
            )
            engineering_task = asyncio.create_task(
                self._calculate_engineering(design_output)
            )
            cost_task = asyncio.create_task(
                self._estimate_costs(design_output)
            )
            
            # Wait for all tasks to complete
            renderings = await render_task
            engineering = await engineering_task
            costs = await cost_task
            
            # Combine all outputs
            complete_design = {
                "design_id": design_output["design_id"],
                "floor_plans": design_output["floor_plans"],
                "elevations": design_output["elevations"],
                "specifications": design_output["specifications"],
                "renderings": renderings,
                "engineering": engineering,
                "costs": costs,
                "metadata": {
                    "input_requirements": requirements,
                    "generation_status": "completed",
                    "service_versions": self._get_service_versions()
                }
            }
            
            # Schedule background tasks for optimization and cleanup
            background_tasks.add_task(self._optimize_design, complete_design)
            background_tasks.add_task(self._cleanup_temporary_files, complete_design["design_id"])
            
            return complete_design
            
        except Exception as e:
            logger.error(f"Error in design generation: {str(e)}")
            raise
            
    async def _generate_design(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate initial design using the design generator."""
        try:
            # Validate requirements
            if not self.design_generator.validate_input(requirements):
                raise ValueError("Invalid input requirements")
                
            # Preprocess input
            input_tensor = self.design_generator.preprocess(requirements)
            
            # Generate design
            design_output = await self.design_generator.generate_async(input_tensor)
            
            # Post-process output
            processed_output = self.design_generator.postprocess(design_output)
            
            return processed_output
            
        except Exception as e:
            logger.error(f"Error in design generation step: {str(e)}")
            raise
            
    async def _process_renderings(self, floor_plans: Dict[str, Any]) -> Dict[str, Any]:
        """Process renderings for the design."""
        try:
            return await self.render_processor.process(floor_plans)
        except Exception as e:
            logger.error(f"Error in rendering processing: {str(e)}")
            return {"error": str(e)}
            
    async def _calculate_engineering(self, design: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate engineering specifications."""
        try:
            return await self.engineering_calculator.calculate(design)
        except Exception as e:
            logger.error(f"Error in engineering calculations: {str(e)}")
            return {"error": str(e)}
            
    async def _estimate_costs(self, design: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate costs for the design."""
        try:
            return await self.cost_estimator.estimate(design)
        except Exception as e:
            logger.error(f"Error in cost estimation: {str(e)}")
            return {"error": str(e)}
            
    async def _optimize_design(self, design: Dict[str, Any]):
        """Optimize design in the background."""
        try:
            # Implement design optimization logic here
            pass
        except Exception as e:
            logger.error(f"Error in design optimization: {str(e)}")
            
    async def _cleanup_temporary_files(self, design_id: str):
        """Clean up temporary files created during design generation."""
        try:
            temp_dir = Path(get_settings().TEMP_DIR) / design_id
            if temp_dir.exists():
                # Implement cleanup logic
                pass
        except Exception as e:
            logger.error(f"Error in cleanup: {str(e)}")
            
    def _get_service_versions(self) -> Dict[str, str]:
        """Get versions of all active services."""
        return {
            "design_generator": self.design_generator.version,
            "render_processor": self.render_processor.version,
            "engineering_calculator": self.engineering_calculator.version,
            "cost_estimator": self.cost_estimator.version
        }
        
    async def get_service_status(self) -> Dict[str, str]:
        """Get current status of all services."""
        return self.service_status.copy()
        
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all services."""
        health_status = {
            "status": "healthy",
            "services": {}
        }
        
        try:
            # Check each service
            health_status["services"]["design_generator"] = await self._check_service_health(self.design_generator)
            health_status["services"]["render_processor"] = await self._check_service_health(self.render_processor)
            health_status["services"]["engineering_calculator"] = await self._check_service_health(self.engineering_calculator)
            health_status["services"]["cost_estimator"] = await self._check_service_health(self.cost_estimator)
            
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["error"] = str(e)
            
        return health_status
        
    async def _check_service_health(self, service: Any) -> Dict[str, Any]:
        """Check health of individual service."""
        try:
            # Implement service-specific health check
            return {
                "status": "healthy",
                "version": getattr(service, "version", "unknown"),
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
