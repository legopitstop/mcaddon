__all__ = ["SpecificEnchantsFunction", "SpecificEnchant"]

from typing import List
from pydantic import Field
from mcaddon.core.base import BaseModel
from .base import LootFunction, BaseLootFunction


class SpecificEnchant(BaseModel):
    id: str
    level: List[int] | int = Field(default_factory=list)


@LootFunction.register
class SpecificEnchantsFunction(BaseLootFunction):
    TYPE_ID = "minecraft:specific_enchants"
    function: str = TYPE_ID

    enchants: List[SpecificEnchant] = Field(default_factory=list)
