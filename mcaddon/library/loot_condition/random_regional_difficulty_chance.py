__all__ = ["RandomRegionalDifficultyChanceCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class RandomRegionalDifficultyChanceCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:random_regional_difficulty_chance"
    condition: str = TYPE_ID

    max_chance: float
