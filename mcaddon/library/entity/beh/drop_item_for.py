__all__ = ["EntityDropItemForComponent"]

from typing import Optional, Tuple, List, ClassVar
from pydantic import Field
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityDropItemForComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drop_item_for)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.drop_item_for"

    cooldown: float = 0.2
    drop_item_chance: float = 1
    entity_types: Optional[EntityType | List[EntityType]] = Field(default_factory=list)
    goal_radius: float = 0.5
    loot_table: Optional[str] = None
    max_head_look_at_height: float = 10
    minimum_teleport_distance: float = 2
    offering_distance: float = 1
    on_drop_attempt: Optional[EntityTriggerEvent] = None
    search_count: int = 1
    search_height: int = 1
    search_range: int = 0
    seconds_before_pickup: float = 0
    speed_multiplier: float = 1
    target_range: Tuple[int, int, int] = (1, 1, 1)
    teleport_offset: Tuple[int, int, int] = (0, 1, 0)
    time_of_day_range: Optional[NumberRange] = None
