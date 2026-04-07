__all__ = ["SpawnRuleSpawnsOnBlockPreventedFilter"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import ValueComponent, BlockLike
from .component import SpawnRuleComponent


@SpawnRuleComponent.register
class SpawnRuleSpawnsOnBlockPreventedFilter(ValueComponent, SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_block_prevented_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawns_on_block_prevented_filter"

    value: List[BlockLike] = Field(default_factory=list)
