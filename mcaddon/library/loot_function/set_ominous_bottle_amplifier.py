__all__ = ["SetOminousBottleAmplifierFunction"]

from mcaddon.core.base import NumberRange
from .base import LootFunction, BaseLootFunction


@LootFunction.register
class SetOminousBottleAmplifierFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_ominous_bottle_amplifier"
    function: str = TYPE_ID

    amplifier: NumberRange
