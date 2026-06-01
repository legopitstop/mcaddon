__all__ = ["RandomChanceWithLootingCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class RandomChanceWithLootingCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:random_chance_with_looting"
    condition: str = TYPE_ID

    chance: float
    looting_multiplier: float
