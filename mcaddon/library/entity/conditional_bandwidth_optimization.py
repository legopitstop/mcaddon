__all__ = ["EntityConditionalBandwidthOptimizationComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field

from mcaddon.library.filter import Filter
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class ConditionalValues(BaseModel):
    conditional_values: List[Filter] = Field(default_factory=list)
    max_dropped_ticks: int = 10
    max_optimized_distance: float = 80
    use_motion_prediction_hints: bool = False


class DefaultValues(BaseModel):
    max_dropped_ticks: int = 10
    max_optimized_distance: float = 80
    use_motion_prediction_hints: bool = False


@EntityComponent.register
class EntityConditionalBandwidthOptimizationComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_conditional_bandwidth_optimization)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:conditional_bandwidth_optimization"

    conditional_values: List[ConditionalValues] = Field(default_factory=list)
    default_values: Optional[DefaultValues] = None
