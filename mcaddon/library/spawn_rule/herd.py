__all__ = ["SpawnRuleHerd", "SpawnRuleHerdData"]

from typing import Optional, List, ClassVar
from pydantic import ConfigDict, Field
from mcaddon.core.base import ValueComponent, BaseModel
from .component import SpawnRuleComponent


class SpawnRuleHerdData(BaseModel):
    event: Optional[str] = None
    event_skip_count: Optional[float] = None
    max_size: float
    min_size: float


@SpawnRuleComponent.register
class SpawnRuleHerd(ValueComponent, SpawnRuleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/herd)
    """

    model_config = ConfigDict(extra="allow")

    COMPONENT_ID: ClassVar[str] = "minecraft:herd"

    value: List[SpawnRuleHerdData] | SpawnRuleHerdData = Field(default_factory=list)
