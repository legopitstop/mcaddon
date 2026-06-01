__all__ = ["LootTableLootEntry"]

from typing import Optional

from .base import LootEntry


class LootTableLootEntry(LootEntry):
    name: str
    quality: Optional[int] = None
