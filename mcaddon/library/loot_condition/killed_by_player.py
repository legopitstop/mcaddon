__all__ = ["KilledByPlayerCondition"]

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class KilledByPlayerCondition(BaseLootCondition):
    TYPE_ID = "minecraft:killed_by_player"
    condition: str = TYPE_ID
