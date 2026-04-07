__all__ = ["SetDataFromColorIndexFunction"]

from .base import LootFunction, BaseLootFunction


@LootFunction.register
class SetDataFromColorIndexFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_data_from_color_index"
    function: str = TYPE_ID
