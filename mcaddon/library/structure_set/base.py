__all__ = ["StructureSet"]

from typing import List, cast
from pydantic import Field

from mcaddon.core.file import ResourceFile
from mcaddon.core.base import BaseModel, BaseTypedModel, TypedModel
from mcaddon.library.common import BaseDescription
from mcaddon.library.pack import behaviorpack


class Placement(BaseTypedModel):
    pass


@Placement.register
class RandomSpreadPlacement(TypedModel):
    TYPE_ID = "minecraft:random_spread"
    type: str = TYPE_ID

    salt: int = 0
    separation: int = 0
    spacing: int = 0
    spread_type: str = "linear"


class Structure(BaseModel):
    structure: str
    weight: int


@behaviorpack("worldgen/structure_sets")
class StructureSet(ResourceFile):
    TYPE_ID = "minecraft:structure_set"

    description: BaseDescription = BaseDescription(identifier="minecraft:structure_set")

    placement: Placement = cast(Placement, RandomSpreadPlacement())
    structures: List[Structure] = Field(default_factory=list)

    @property
    def id(self) -> str:
        return self.description.identifier
