__all__ = ["EntityTradeTableComponent"]

from typing import Optional, ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityTradeTableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trade_table)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:trade_table"

    convert_trades_economy: bool = False
    display_name: Optional[str] = None
    new_screen: bool = False
    persist_trades: bool = False
    table: Optional[str] = None
