__all__ = ["HasVariantCondition"]

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class HasVariantCondition(BaseLootCondition):
    TYPE_ID = "minecraft:has_variant"
    condition: str = TYPE_ID

    value: int
