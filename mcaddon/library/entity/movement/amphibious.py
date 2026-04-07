__all__ = ["EntityMovementAmphibiousComponent"]

from mcaddon.library.entity.component import EntityComponent
from typing import ClassVar
from .base import EntityBaseMovementComponent


@EntityComponent.register
class EntityMovementAmphibiousComponent(EntityBaseMovementComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.amphibious)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movement.amphibious"
