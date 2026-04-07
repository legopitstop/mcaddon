__all__ = ["EntityFloatTemptComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityFloatTemptComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float_tempt)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.float_tempt"

    can_get_scared: bool = False
    can_tempt_vertically: bool = False
    can_tempt_while_ridden: bool = False
    items: List[str] = Field(default_factory=list)
    on_tempt_end: Optional[EntityTriggerEvent] = None
    sound_interval: Optional[NumberRange] = None
    speed_multiplier: float = 1
    stop_distance: float = 1.5
    tempt_sound: Optional[str] = None
    within_radius: float = 0
