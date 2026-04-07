__all__ = ["EntityTradeResupplyComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityTradeResupplyComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trade_resupply)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:trade_resupply"
