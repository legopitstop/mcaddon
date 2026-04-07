__all__ = ["EntityIsShakingComponent"]

from mcaddon.library.filter import FilterTest
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityIsShakingComponent(EntityComponent, FilterTest):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_shaking)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:is_shaking"
