__all__ = ["EntityAvoidBlockComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityAvoidBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_avoid_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.avoid_block"

    avoid_block_sound: Optional[str] = None
    on_escape: Optional[EntityTriggerEvent | List[EntityTriggerEvent]] = None
    search_height: int = 0
    search_range: int = 0
    sound_interval: Optional[NumberRange] = None
    sprint_speed_modifier: float = 1
    target_blocks: List[str] = Field(default_factory=list)
    target_selection_method: str = "nearest"
    tick_interval: int = 1
    walk_speed_modifier: float = 1
