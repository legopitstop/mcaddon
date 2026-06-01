__all__ = ["ItemLootEntry"]

from typing import List

from mcaddon.library.loot_table import LootPool
from mcaddon.library.loot_function import LootFunction
from mcaddon.library.loot_condition import LootCondition
from .base import LootEntry


class ItemLootEntry(LootEntry):
    name: str
    functions: List[LootFunction] = ...
    conditions: List[LootCondition] = ...
    pools: List["LootPool"] = ...
