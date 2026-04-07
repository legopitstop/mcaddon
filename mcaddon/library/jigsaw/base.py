__all__ = [
    "Jigsaw",
    "MaxDistanceFromCenter",
    "StartHeight",
    "ConstantStartHeight",
    "ConstantStartHeightValue",
]

from typing import List, ClassVar, Any
from pydantic import Field, field_validator

from mcaddon.core.base import BaseModel, BaseTypedModel, TypedModel
from mcaddon.core.file import ResourceFile
from mcaddon.library.filter import Filter
from mcaddon.library.common import BaseDescription
from mcaddon.library.pack import behaviorpack


class StartHeight(BaseTypedModel):
    pass


class ConstantStartHeightValue(BaseModel):
    absolute: int


@StartHeight.register
class ConstantStartHeight(TypedModel):
    TYPE_ID: ClassVar[str] = "constant"
    type: str = TYPE_ID

    value: ConstantStartHeightValue = Field(
        default_factory=lambda: ConstantStartHeightValue(absolute=1)
    )


class MaxDistanceFromCenter(BaseModel):
    horizontal: int
    vertical: int


@behaviorpack("worldgen/structures")
class Jigsaw(ResourceFile):
    TYPE_ID = "minecraft:jigsaw"

    description: BaseDescription = BaseDescription(identifier="minecraft:jigsaw")

    biome_filters: List[Filter] = Field(default_factory=list)

    step: str = "underground_structures"
    terrain_adaptation: str = "bury"
    start_pool: str = "minecraft:default"
    max_depth: int = 7
    heightmap_projection: str = "world_surface"
    start_height: TypedModel = Field(default_factory=ConstantStartHeight)
    max_distance_from_center: MaxDistanceFromCenter = MaxDistanceFromCenter(
        horizontal=1, vertical=1
    )

    @field_validator("start_height", mode="wrap")
    @classmethod
    def deserialize_start_height(cls, v: Any, handler) -> Any:
        """Handle polymorphic deserialization of start_height based on type field."""
        if isinstance(v, dict):
            type_id = v.get("type", "constant")
            if type_id in StartHeight.__all__:
                model_class = StartHeight.__all__[type_id]
                return model_class.model_validate(v)
        return handler(v)

    @property
    def id(self) -> str:
        return self.description.identifier
