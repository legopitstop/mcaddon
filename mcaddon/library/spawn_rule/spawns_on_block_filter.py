__all__ = ["SpawnRuleSpawnsOnBlockFilter"]


from typing import List, ClassVar

from pydantic import Field

from mcaddon.core.base import BlockLike, ValueComponent
from .component import SpawnRuleComponent


@SpawnRuleComponent.register
class SpawnRuleSpawnsOnBlockFilter(ValueComponent, SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_block_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:spawns_on_block_filter"

    value: List[BlockLike] | BlockLike = Field(default_factory=list)
