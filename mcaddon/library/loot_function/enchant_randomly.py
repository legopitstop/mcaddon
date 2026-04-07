__all__ = ["EnchantRandomlyFunction"]

from typing import Optional
from .base import LootFunction, BaseLootFunction


@LootFunction.register
class EnchantRandomlyFunction(BaseLootFunction):
    TYPE_ID = "minecraft:enchant_randomly"
    function: str = TYPE_ID

    treasure: Optional[bool] = None
