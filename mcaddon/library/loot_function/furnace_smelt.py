__all__ = ["FurnaceSmeltFunction"]

from typing import List
from pydantic import Field
from .base import LootFunction, BaseLootFunction
from mcaddon.library.loot_condition import LootCondition


@LootFunction.register
class FurnaceSmeltFunction(BaseLootFunction):
    TYPE_ID = "minecraft:furnace_smelt"
    function: str = TYPE_ID

    conditions: List[LootCondition] = Field(default_factory=list)
