__all__ = ["EntityIsPregnantComponent"]

from mcaddon.library.filter import FilterTest
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityIsPregnantComponent(EntityComponent, FilterTest):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_pregnant)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:is_pregnant"
