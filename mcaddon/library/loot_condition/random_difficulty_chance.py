__all__ = ["RandomDifficultyChanceCondition"]

from typing import Optional, ClassVar
from .base import LootCondition, BaseLootCondition


@LootCondition.register
class RandomDifficultyChanceCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:random_difficulty_chance"
    condition: str = TYPE_ID

    default_chance: float
    peaceful: Optional[float] = None
    hard: Optional[float] = None
    easy: Optional[float] = None
