__all__ = ["EntityCelebrateComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityCelebrateComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_celebrate)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.celebrate"

    celebration_sound: Optional[str] = None
    duration: float = 30
    jump_interval: Optional[NumberRange] = None
    on_celebration_end_event: Optional[EntityTriggerEvent] = None
    sound_interval: Optional[NumberRange] = None
