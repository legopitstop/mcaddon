__all__ = ["EntityTimerFlag1Component"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityTimerFlag1Component(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_1)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.timer_flag_1"

    control_flags: List[str] = Field(default_factory=list)
    cooldown_range: Optional[NumberRange | float] = None
    duration_range: Optional[NumberRange | float] = None
    on_end: Optional[EntityTriggerEvent] = None
    on_start: Optional[EntityTriggerEvent] = None
