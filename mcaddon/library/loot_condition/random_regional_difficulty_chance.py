__all__ = ["RandomRegionalDifficultyChanceCondition"]

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class RandomRegionalDifficultyChanceCondition(BaseLootCondition):
    TYPE_ID = "minecraft:random_regional_difficulty_chance"
    condition: str = TYPE_ID

    max_chance: float
