__all__ = ["SpawnRuleHeightFilter"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleHeightFilter(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/height_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:height_filter"

    max: int
    min: int
