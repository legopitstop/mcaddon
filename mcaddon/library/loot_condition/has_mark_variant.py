__all__ = ["HasMarkVariantCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class HasMarkVariantCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:has_mark_variant"
    condition: str = TYPE_ID

    value: int
