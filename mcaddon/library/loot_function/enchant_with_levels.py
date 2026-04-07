__all__ = ["EnchantWithLevelsFunction"]

from typing import Optional
from mcaddon.core.base import NumberRange
from .base import LootFunction, BaseLootFunction


@LootFunction.register
class EnchantWithLevelsFunction(BaseLootFunction):
    TYPE_ID = "minecraft:enchant_with_levels"
    function: str = TYPE_ID

    treasure: Optional[bool] = None
    levels: NumberRange | int
