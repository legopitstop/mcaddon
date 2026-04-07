__all__ = ["EnchantBookForTradingFunction"]

from typing import List, Optional
from pydantic import Field
from mcaddon.core.base import BaseModel
from .base import LootFunction, BaseLootFunction


class BookEnchantment(BaseModel):
    name: str
    min: int
    max: int


@LootFunction.register
class EnchantBookForTradingFunction(BaseLootFunction):
    TYPE_ID = "minecraft:enchant_book_for_trading"
    function: str = TYPE_ID

    base_cost: Optional[int] = None
    base_random_cost: Optional[int] = None
    per_level_random_cost: Optional[int] = None
    per_level_cost: Optional[int] = None

    enchantments: List[BookEnchantment] = Field(default_factory=list)
