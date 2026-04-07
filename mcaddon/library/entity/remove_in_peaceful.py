__all__ = ["EntityRemoveInPeacefulComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityRemoveInPeacefulComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_remove_in_peaceful)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:remove_in_peaceful"
