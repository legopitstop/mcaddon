__all__ = ["EntityFleeSunComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityFleeSunComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_flee_sun)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.flee_sun"

    speed_multiplier: float = 1
