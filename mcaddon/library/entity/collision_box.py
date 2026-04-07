__all__ = ["EntityCollisionBoxComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityCollisionBoxComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_collision_box)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:collision_box"

    width: float = 1
    height: float = 1
