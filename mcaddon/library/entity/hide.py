__all__ = ["EntityHideComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityHideComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_hide)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:hide"
