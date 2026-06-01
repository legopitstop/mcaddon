__all__ = ["KilledByEntityCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class KilledByEntityCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:killed_by_entity"
    condition: str = TYPE_ID

    entity_type: str
