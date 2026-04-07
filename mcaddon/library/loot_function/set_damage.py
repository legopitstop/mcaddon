__all__ = ["SetDamageFunction"]

from typing import Optional
from .base import LootFunction, BaseLootFunction
from mcaddon.core.base import NumberRange


@LootFunction.register
class SetDamageFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_damage"
    function: str = TYPE_ID

    damage: NumberRange | int
    add: Optional[bool] = None
