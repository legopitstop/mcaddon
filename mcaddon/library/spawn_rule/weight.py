__all__ = ["SpawnRuleWeight"]

from typing import Optional, ClassVar
from .component import SpawnRuleComponent


@SpawnRuleComponent.register
class SpawnRuleWeight(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/weight)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:weight"

    default: int
    rarity: Optional[int] = None
