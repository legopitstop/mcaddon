__all__ = ["SetDataFunction"]

from mcaddon.core.base import NumberRange
from .base import LootFunction, BaseLootFunction


@LootFunction.register
class SetDataFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_data"
    function: str = TYPE_ID

    data: NumberRange | int
