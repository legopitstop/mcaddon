__all__ = ["EntityIsStunnedComponent"]

from mcaddon.library.filter import FilterTest
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityIsStunnedComponent(EntityComponent, FilterTest):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_stunned)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:is_stunned"
