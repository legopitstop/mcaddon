__all__ = ["KilledByPlayerOrPetsCondition"]

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class KilledByPlayerOrPetsCondition(BaseLootCondition):
    TYPE_ID = "minecraft:killed_by_player_or_pets"
    condition: str = TYPE_ID
