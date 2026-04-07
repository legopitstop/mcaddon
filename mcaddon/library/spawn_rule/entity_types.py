__all__ = ["SpawnRuleEntityTypes"]


from typing import List, ClassVar

from pydantic import Field

from mcaddon.library.filter import Filter
from .component import SpawnRuleComponent


@SpawnRuleComponent.register
class SpawnRuleEntityTypes(SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/entity_types)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:entity_types"

    filters: List[Filter] = Field(default_factory=list)
    max_dist: float = 16
    must_see: bool = False
    must_see_forget_duration: float = 3.0
    sprint_speed_multiplier: float = 1.0
    walk_speed_multiplier: float = 1.0
