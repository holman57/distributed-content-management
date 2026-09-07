"""
Pipeline Instance Registry for the System of Spawning Systems.
"""

from typing import Dict, List, Optional
from ..pipeline.instance import NichePipelineInstance
from ..models.niche import NicheLifecycleState


class PipelineRegistry:
    """
    Maintains active, incubating, scaled, and decommissioned niche pipeline instances.
    """

    def __init__(self):
        self._instances: Dict[str, NichePipelineInstance] = {}

    def register(self, instance: NichePipelineInstance) -> None:
        """Adds a newly spawned pipeline instance to the registry."""
        self._instances[instance.niche.id] = instance

    def get(self, niche_id: str) -> Optional[NichePipelineInstance]:
        """Retrieves a pipeline instance by niche ID."""
        return self._instances.get(niche_id)

    def list_all(self) -> List[NichePipelineInstance]:
        """Returns all registered instances."""
        return list(self._instances.values())

    def list_by_state(self, state: NicheLifecycleState) -> List[NichePipelineInstance]:
        """Filters instances by their current lifecycle state."""
        return [inst for inst in self._instances.values() if inst.niche.state == state]

    def list_active(self) -> List[NichePipelineInstance]:
        """Returns all non-sunset pipeline instances."""
        return [inst for inst in self._instances.values() if inst.niche.state != NicheLifecycleState.SUNSET]
