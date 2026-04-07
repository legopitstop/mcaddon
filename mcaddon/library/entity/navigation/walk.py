__all__ = ["EntityNavigationWalkComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent
from .generic import EntityNavigationGenericComponent


@EntityComponent.register
class EntityNavigationWalkComponent(EntityNavigationGenericComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.walk)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:navigation.walk"

    can_float: Optional[bool] = None
