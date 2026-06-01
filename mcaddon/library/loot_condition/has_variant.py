__all__ = ["HasVariantCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class HasVariantCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:has_variant"
    condition: str = TYPE_ID

    value: int
