__all__ = ["EntityIsIgnitedComponent"]

from mcaddon.library.filter import FilterTest
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityIsIgnitedComponent(EntityComponent, FilterTest):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_ignited)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:is_ignited"
