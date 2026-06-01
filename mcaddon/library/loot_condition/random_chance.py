__all__ = ["RandomChanceCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class RandomChanceCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:random_chance"
    condition: str = TYPE_ID

    chance: float
