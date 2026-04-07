__all__ = ["SpawnRuleDifficultyFilter"]

from typing import Optional, ClassVar
from .component import SpawnRuleComponent


@SpawnRuleComponent.register
class SpawnRuleDifficultyFilter(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/difficulty_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:difficulty_filter"

    max: Optional[str] = None
    min: Optional[str] = None
