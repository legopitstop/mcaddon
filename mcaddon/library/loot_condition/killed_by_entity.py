__all__ = ["KilledByEntityCondition"]

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class KilledByEntityCondition(BaseLootCondition):
    TYPE_ID = "minecraft:killed_by_entity"
    condition: str = TYPE_ID

    entity_type: str
