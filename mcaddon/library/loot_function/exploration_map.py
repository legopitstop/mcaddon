__all__ = ["ExplorationMapFunction"]

from .base import LootFunction, BaseLootFunction


@LootFunction.register
class ExplorationMapFunction(BaseLootFunction):
    TYPE_ID = "minecraft:exploration_map"
    function: str = TYPE_ID

    destination: str
