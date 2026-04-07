__all__ = ["EntityRandomSwimComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRandomSwimComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_swim)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_swim"

    avoid_surface: bool = True
    interval: int = 120
    speed_multiplier: float = 1
    xz_dist: int = 10
    y_dist: int = 7
