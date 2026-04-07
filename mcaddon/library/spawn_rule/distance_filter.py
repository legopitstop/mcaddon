__all__ = ["SpawnRuleDistanceFilter"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleDistanceFilter(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/distance_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:distance_filter"

    max: int = 128
    min: int = 24
