__all__ = ["SpawnRule", "SpawnRuleDescription"]

from typing import List, Dict, Any
from pydantic import Field

from mcaddon.library.pack import behaviorpack
from mcaddon.library.common import BaseDescription
from mcaddon.core.base import BaseModel, ComponentSet
from mcaddon.core.file import ResourceFile
from .component import SpawnRuleComponent


class SpawnRuleDescription(BaseDescription):
    population_control: str


@behaviorpack("spawn_rules")
class SpawnRule(ResourceFile, BaseModel):
    TYPE_ID = "minecraft:spawn_rules"
    format_version: str = "1.17.0"

    description: SpawnRuleDescription = SpawnRuleDescription(
        identifier="minecraft:default_spawn_rules", population_control="monster"
    )
    conditions: List[ComponentSet[SpawnRuleComponent]] = Field(default_factory=list)
    events: Dict[str, Any] = Field(default_factory=dict)

    @property
    def id(self) -> str:
        return self.description.identifier
