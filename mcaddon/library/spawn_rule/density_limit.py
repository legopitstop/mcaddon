__all__ = ["SpawnRuleDensityLimit"]

from typing import Optional, ClassVar
from .component import SpawnRuleComponent


@SpawnRuleComponent.register
class SpawnRuleDensityLimit(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/density_limit)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:density_limit"

    surface: Optional[int] = None
    underground: Optional[int] = None
