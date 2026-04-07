__all__ = ["EntityGlideMovementComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityGlideMovementComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_glide_movement)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:glide_movement"
