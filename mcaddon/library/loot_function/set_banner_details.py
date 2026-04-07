__all__ = ["SetBannerDetailsFunction"]

from .base import LootFunction, BaseLootFunction


@LootFunction.register
class SetBannerDetailsFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_banner_details"
    function: str = TYPE_ID

    type: int
