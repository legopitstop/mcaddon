__all__ = ["EnchantRandomGearFunction"]

from .base import LootFunction, BaseLootFunction


@LootFunction.register
class EnchantRandomGearFunction(BaseLootFunction):
    TYPE_ID = "minecraft:enchant_random_gear"
    function: str = TYPE_ID

    chance: float
