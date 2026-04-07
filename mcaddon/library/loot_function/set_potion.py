__all__ = ["SetPotionFunction"]

from .base import LootFunction, BaseLootFunction


@LootFunction.register
class SetPotionFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_potion"
    function: str = TYPE_ID

    id: str
