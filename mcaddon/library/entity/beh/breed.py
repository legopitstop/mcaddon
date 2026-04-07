__all__ = ["EntityBreedComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityBreedComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_breed)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.breed"

    speed_multiplier: float = 1
