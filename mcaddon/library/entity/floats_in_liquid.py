__all__ = ["EntityFloatsInLiquidComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityFloatsInLiquidComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_floats_in_liquid)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:floats_in_liquid"
