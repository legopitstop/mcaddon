__all__ = ["SetCountFunction"]

from typing import Optional
from .base import LootFunction, BaseLootFunction
from mcaddon.core.base import NumberRange


@LootFunction.register
class SetCountFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_count"
    function: str = TYPE_ID

    count: NumberRange | int
    add: Optional[bool] = None
