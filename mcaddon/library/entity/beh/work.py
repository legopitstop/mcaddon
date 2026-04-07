__all__ = ["EntityWorkComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityWorkComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_work)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.work"

    active_time: int = 0
    can_work_in_rain: bool = False
    goal_cooldown: int = 0
    on_arrival: Optional[EntityTriggerEvent] = None
    sound_delay_max: int = 0
    sound_delay_min: int = 0
    speed_multiplier: float = 0.5
    work_in_rain_tolerance: int = -1
