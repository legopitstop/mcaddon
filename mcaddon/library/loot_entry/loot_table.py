__all__ = ["LootTableLootEntry"]

from typing import Optional, ClassVar

from .base import LootEntry


@LootEntry.register
class LootTableLootEntry(LootEntry):
    TYPE_ID: ClassVar[str] = "loot_table"
    type: str = 'loot_table'

    name: str
    quality: Optional[int] = None
