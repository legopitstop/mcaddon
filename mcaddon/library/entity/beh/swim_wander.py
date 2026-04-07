__all__ = ["EntitySwimWanderComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySwimWanderComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_wander)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.swim_wander"

    interval: float = 0.00833
    look_ahead: float = 5
    speed_multiplier: float = 1
    wander_time: float = 5
