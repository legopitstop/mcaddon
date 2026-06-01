__all__ = ["Trading", "TradeTier", "TradeGroup", "Trade", "TradeItem", "TradeChoice"]

from typing import List, Optional
from pydantic import Field

from mcaddon.core.file import JsonFile
from mcaddon.core.base import NumberRange, BaseModel
from mcaddon.library.filter import Filter
from mcaddon.library.loot_table import LootFunction
from mcaddon.library.pack import behaviorpack


class TradeItem(BaseModel):
    item: str
    quantity: Optional[int | NumberRange] = None
    price_multiplier: Optional[float] = None
    functions: List[LootFunction] = Field(default_factory=list)
    filters: Optional[Filter] = None


class TradeChoice(BaseModel):
    choice: List[TradeItem] = Field(default_factory=list)


class Trade(BaseModel):
    wants: List[TradeItem | TradeChoice] = Field(default_factory=list)
    gives: List[TradeItem | TradeChoice] = Field(default_factory=list)
    trader_exp: Optional[int] = None
    max_uses: Optional[int] = None
    reward_exp: Optional[int] = None


class TradeGroup(BaseModel):
    num_to_select: Optional[int] = None
    trades: List[Trade] = Field(default_factory=list)


class TradeTier(TradeGroup):
    total_exp_required: Optional[int] = None
    trades: List[Trade] = Field(default_factory=list)
    groups: List[TradeGroup] = Field(default_factory=list)


@behaviorpack("trading")
class Trading(JsonFile):
    tiers: List[TradeTier] = Field(default_factory=list)
