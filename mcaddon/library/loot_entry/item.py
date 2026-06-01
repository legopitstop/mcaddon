__all__ = ["ItemLootEntry"]

from typing import List, ClassVar
from pydantic import Field

from mcaddon.library.loot_table import LootPool
from mcaddon.library.loot_function import LootFunction
from mcaddon.library.loot_condition import LootCondition
from .base import LootEntry


@LootEntry.register
class ItemLootEntry(LootEntry):
    TYPE_ID: ClassVar[str] = "item"
    type: str = 'item'

    name: str
    functions: List[LootFunction] = Field(default_factory=list)
    conditions: List[LootCondition] = Field(default_factory=list)
    pools: List["LootPool"] = Field(default_factory=list)
