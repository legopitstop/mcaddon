__all__ = ["EntityColorComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityColorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_color)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:color"

    value: int
