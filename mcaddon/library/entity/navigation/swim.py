__all__ = ["EntityNavigationSwimComponent"]

from mcaddon.library.entity.component import EntityComponent
from typing import ClassVar
from .generic import EntityNavigationGenericComponent


@EntityComponent.register
class EntityNavigationSwimComponent(EntityNavigationGenericComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.swim)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:navigation.swim"
