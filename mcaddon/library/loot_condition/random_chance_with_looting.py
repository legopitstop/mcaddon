__all__ = ["RandomChanceWithLootingCondition"]

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class RandomChanceWithLootingCondition(BaseLootCondition):
    TYPE_ID = "minecraft:random_chance_with_looting"
    condition: str = TYPE_ID

    chance: float
    looting_multiplier: float
