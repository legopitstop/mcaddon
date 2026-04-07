__all__ = ["SpawnRuleBiomeFilter"]

from typing import List, ClassVar
from pydantic import ConfigDict, Field

from mcaddon.core.base import ValueComponent
from mcaddon.library.filter import Filter
from .component import SpawnRuleComponent


@SpawnRuleComponent.register
class SpawnRuleBiomeFilter(ValueComponent, SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/biome_filter)
    """

    model_config = ConfigDict(extra="allow")

    COMPONENT_ID: ClassVar[str] = "minecraft:biome_filter"

    value: Filter | str | List[Filter] = Field(default_factory=list)
