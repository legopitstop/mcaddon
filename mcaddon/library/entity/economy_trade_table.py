__all__ = ["EntityEconomyTradeTableComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field

from mcaddon.core.base import NumberRange
from .component import EntityComponent


@EntityComponent.register
class EntityEconomyTradeTableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_economy_trade_table)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:economy_trade_table"

    convert_trades_economy: bool = False
    cured_discount: List[int] = Field(default_factory=list)
    display_name: Optional[str] = None
    hero_demand_discount: int = -4
    max_cured_discount: Optional[int | NumberRange] = None
    max_nearby_cured_discount: int = -200
    nearby_cured_discount: int = -20
    new_screen: bool = False
    persist_trades: bool = False
    show_trade_screen: bool = True
    table: Optional[str] = None
    use_legacy_price_formula: bool = False
