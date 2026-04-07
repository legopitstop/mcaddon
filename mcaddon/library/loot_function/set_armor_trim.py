__all__ = ["SetArmorTrimFunction"]

from .base import LootFunction, BaseLootFunction


@LootFunction.register
class SetArmorTrimFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_armor_trim"
    function: str = TYPE_ID

    material: str
    pattern: str
