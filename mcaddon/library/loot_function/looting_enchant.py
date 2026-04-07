__all__ = ["LootingEnchantFunction"]

from typing import Optional
from mcaddon.core.base import NumberRange
from .base import LootFunction, BaseLootFunction


@LootFunction.register
class LootingEnchantFunction(BaseLootFunction):
    TYPE_ID = "minecraft:looting_enchant"
    function: str = TYPE_ID

    count: NumberRange
    limit: Optional[int] = None
