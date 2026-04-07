__all__ = ["SetStewEffectFunction"]

from typing import List
from pydantic import Field
from mcaddon.core.base import StatusEffect
from .base import LootFunction, BaseLootFunction


@LootFunction.register
class SetStewEffectFunction(BaseLootFunction):
    TYPE_ID = "minecraft:set_stew_effect"
    function: str = TYPE_ID

    effects: List[StatusEffect] = Field(default_factory=list)
