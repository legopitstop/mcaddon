__all__ = ["EntityNavigationHoverComponent"]

from mcaddon.library.entity.component import EntityComponent
from typing import ClassVar
from .generic import EntityNavigationGenericComponent


@EntityComponent.register
class EntityNavigationHoverComponent(EntityNavigationGenericComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.hover)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:navigation.hover"
