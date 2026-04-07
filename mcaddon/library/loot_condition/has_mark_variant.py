__all__ = ["HasMarkVariantCondition"]

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class HasMarkVariantCondition(BaseLootCondition):
    TYPE_ID = "minecraft:has_mark_variant"
    condition: str = TYPE_ID

    value: int
