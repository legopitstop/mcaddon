__all__ = ["EntityIsSaddledComponent"]

from mcaddon.library.filter import FilterTest
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityIsSaddledComponent(EntityComponent, FilterTest):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_saddled)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:is_saddled"
