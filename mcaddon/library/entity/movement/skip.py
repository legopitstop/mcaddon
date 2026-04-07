__all__ = ["EntityMovementSkipComponent"]

from mcaddon.library.entity.component import EntityComponent
from typing import ClassVar
from .base import EntityBaseMovementComponent


@EntityComponent.register
class EntityMovementSkipComponent(EntityBaseMovementComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.skip)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movement.skip"
