__all__ = ["RandomDyeFunction"]

from .base import LootFunction, BaseLootFunction


@LootFunction.register
class RandomDyeFunction(BaseLootFunction):
    TYPE_ID = "minecraft:random_dye"
    function: str = TYPE_ID
