__all__ = ["EntitySleepComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntitySleepComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sleep)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.sleep"

    can_sleep_while_riding: bool = False
    cooldown_time: float = 0
    goal_radius: Optional[float] = None
    sleep_collider_height: float = 1
    sleep_collider_width: float = 1
    sleep_y_offset: float = 1
    speed_multiplier: float = 1
    timeout_cooldown: float = 8
