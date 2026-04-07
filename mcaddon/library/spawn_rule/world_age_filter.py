__all__ = ["SpawnRuleWorldAgeFilter"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRuleWorldAgeFilter(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/world_age_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:world_age_filter"

    min: int
