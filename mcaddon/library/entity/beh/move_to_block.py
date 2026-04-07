__all__ = ["EntityMoveToBlockComponent", "SelectionMethod"]

from typing import Optional, List, ClassVar
from pydantic import Field
from enum import Enum

from mcaddon.library.filter import Filter
from mcaddon.core.types import Vector3
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


class SelectionMethod(Enum):
    Random = "random"
    Nearest = "nearest"


@EntityComponent.register
class EntityMoveToBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_to_block"

    goal_radius: float = 0.5
    on_reach: Optional[EntityTriggerEvent | List[EntityTriggerEvent]] = None
    on_stay_completed: Optional[EntityTriggerEvent | List[EntityTriggerEvent]] = None
    search_height: int = 1
    search_range: int = 0
    speed_multiplier: float = 1
    start_chance: float = 1
    stay_duration: float = 0
    target_block_filters: Optional[Filter] = None
    target_blocks: List[str] = Field(default_factory=list)
    target_offset: Vector3 = (0, 0, 0)
    target_selection_method: SelectionMethod = SelectionMethod.Nearest
    tick_interval: int = 20
