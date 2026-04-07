__all__ = ["RandomAuxValueFunction"]

from .base import LootFunction, BaseLootFunction
from mcaddon.core.base import NumberRange


@LootFunction.register
class RandomAuxValueFunction(BaseLootFunction):
    TYPE_ID = "minecraft:random_aux_value"
    function: str = TYPE_ID

    values: NumberRange
