__all__ = ["KilledByPlayerCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class KilledByPlayerCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:killed_by_player"
    condition: str = TYPE_ID
