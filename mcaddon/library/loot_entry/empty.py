__all__ = ["EmptyLootEntry"]

from typing import ClassVar

from .base import LootEntry


@LootEntry.register
class EmptyLootEntry(LootEntry):
    TYPE_ID: ClassVar[str] = "empty"
    type: str = 'empty'
