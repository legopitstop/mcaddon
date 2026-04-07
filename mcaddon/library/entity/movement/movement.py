__all__ = ["EntityMovementComponent"]

from mcaddon.library.entity.component import EntityAttributeComponent, EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityMovementComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movement"
