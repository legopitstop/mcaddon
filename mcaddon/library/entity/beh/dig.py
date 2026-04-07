__all__ = ["EntityDigComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityDigComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dig)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.dig"

    allow_dig_when_named: bool = False
    digs_in_daylight: bool = False
    duration: float = 0
    idle_time: float = 0
    on_start: Optional[EntityTriggerEvent] = None
    suspicion_is_disturbance: bool = False
    vibration_is_disturbance: bool = False
