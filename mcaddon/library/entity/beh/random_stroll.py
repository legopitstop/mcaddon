__all__ = ["EntityRandomStrollComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRandomStrollComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_stroll)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_stroll"
    interval: int = 100
    speed_multiplier: float = 1
    xz_dist: int = 10
    y_dist: int = 7
