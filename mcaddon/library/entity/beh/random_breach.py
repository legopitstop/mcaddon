__all__ = ["EntityRandomBreachComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRandomBreachComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_breach)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_breach"

    cooldown_time: float = 0
    interval: int = 120
    speed_multiplier: float = 1
    xz_dist: int = 10
    y_dist: int = 7
