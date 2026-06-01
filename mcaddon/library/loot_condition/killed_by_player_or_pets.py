__all__ = ["KilledByPlayerOrPetsCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class KilledByPlayerOrPetsCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:killed_by_player_or_pets"
    condition: str = TYPE_ID
