__all__ = [
    "LootTable",
    "LootFunction",
    "LootCondition",
    "LootPool",
    "LootPoolTiers",
]

from typing import List, Optional, Any
from pydantic import Field

from mcaddon.core.file import JsonFile
from mcaddon.core.base import BaseModel, NumberRange
from mcaddon.library.loot_entry import LootEntry
from mcaddon.library.loot_function import LootFunction
from mcaddon.library.loot_condition import LootCondition
from .pack import behaviorpack


class LootPoolTiers(BaseModel):
    initial_range: int
    bonus_rolls: Optional[int] = None
    bonus_chance: Optional[float] = None


class LootPool(BaseModel):
    rolls: Optional[int | NumberRange] = None
    bonus_rolls: Optional[int | NumberRange] = None
    entries: List[LootEntry] = Field(default_factory=list)
    tiers: Optional[LootPoolTiers] = None

    functions: List[Any] = Field(default_factory=list)
    conditions: List[Any] = Field(default_factory=list)


@behaviorpack("loot_tables")
class LootTable(JsonFile):
    pools: List[LootPool] = Field(default_factory=list)
    type: Optional[str] = None

    @staticmethod
    def block(name: str) -> "LootTable":
        from mcaddon.library.loot_entry import ItemLootEntry

        return LootTable(
            type="block", pools=[LootPool(entries=[ItemLootEntry(name=name)])]
        )
