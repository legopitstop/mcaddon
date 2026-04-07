__all__ = ["EntityIsIllagerCaptainComponent"]

from mcaddon.library.filter import FilterTest
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityIsIllagerCaptainComponent(EntityComponent, FilterTest):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_illager_captain)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:is_illager_captain"
