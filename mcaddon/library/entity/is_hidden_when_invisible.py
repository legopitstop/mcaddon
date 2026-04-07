__all__ = ["EntityIsHiddenWhenInvisibleComponent"]

from mcaddon.library.filter import FilterTest
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityIsHiddenWhenInvisibleComponent(EntityComponent, FilterTest):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_hidden_when_invisible)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:is_hidden_when_invisible"
