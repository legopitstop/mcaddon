__all__ = ["SpawnRulePlayerInVillageFilter"]


from .component import SpawnRuleComponent
from typing import ClassVar


@SpawnRuleComponent.register
class SpawnRulePlayerInVillageFilter(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/player_in_village_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:player_in_village_filter"

    distance: int
    village_border_tolerance: int
