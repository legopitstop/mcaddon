__all__ = ["EntityKilledCondition"]

from typing import ClassVar

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class EntityKilledCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:entity_killed"
    condition: str = TYPE_ID

    entity_type: str
