__all__ = ["EntityItemHopperComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityItemHopperComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_item_hopper)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:item_hopper"
