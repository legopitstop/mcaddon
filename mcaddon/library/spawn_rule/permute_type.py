__all__ = ["SpawnRulePermuteType"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import ValueComponent, BaseModel
from .component import SpawnRuleComponent


class SpawnRulePermuteTypeData(BaseModel):
    weight: int
    entity_type: Optional[str] = None
    guaranteed_count: Optional[int] = None


@SpawnRuleComponent.register
class SpawnRulePermuteType(ValueComponent, SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/permute_type)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:permute_type"

    value: List[SpawnRulePermuteTypeData] | SpawnRulePermuteTypeData = Field(
        default_factory=list
    )
