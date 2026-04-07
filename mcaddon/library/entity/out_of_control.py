__all__ = ["EntityOutOfControlComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityOutOfControlComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_out_of_control)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:out_of_control"
