__all__ = ["RandomChanceCondition"]

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class RandomChanceCondition(BaseLootCondition):
    TYPE_ID = "minecraft:random_chance"
    condition: str = TYPE_ID

    chance: float
