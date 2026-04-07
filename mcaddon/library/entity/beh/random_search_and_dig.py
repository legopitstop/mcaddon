__all__ = ["EntityRandomSearchAndDigComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityRandomSearchAndDigComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_search_and_dig)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_search_and_dig"

    cooldown_range: Optional[NumberRange | float] = None
    digging_duration_range: Optional[NumberRange] = None
    find_valid_position_retries: int = 5
    goal_radius: float = 1.5
    item_table: Optional[str] = None
    on_digging_start: Optional[EntityTriggerEvent] = None
    on_fail_during_digging: Optional[EntityTriggerEvent] = None
    on_fail_during_searching: Optional[EntityTriggerEvent] = None
    on_item_found: Optional[EntityTriggerEvent] = None
    on_searching_start: Optional[EntityTriggerEvent] = None
    on_success: Optional[EntityTriggerEvent] = None
    search_range_xz: int = 10
    search_range_y: int = 7
    spawn_item_after_seconds: float = 0
    spawn_item_pos_offset: float = 0
    speed_multiplier: float = 1
    target_blocks: List[str] = Field(default_factory=list)
    target_dig_position_offset: float = 2.25
