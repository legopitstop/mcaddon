__all__ = ["EntityCelebrateSurviveComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityCelebrateSurviveComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_celebrate_survive)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.celebrate_survive"

    duration: float = 30
    fireworks_interval: Optional[NumberRange] = None
    on_celebration_end_event: Optional[EntityTriggerEvent] = None
