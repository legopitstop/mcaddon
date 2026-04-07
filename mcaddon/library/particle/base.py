__all__ = [
    "Particle",
    "ParticleDescription",
    "BasicRenderParameters",
]

from typing import Dict, Any, List
from pydantic import Field, field_validator

from mcaddon.library.pack import resourcepack
from mcaddon.library.common import BaseDescription
from mcaddon.library.constants import CurveType
from mcaddon.core.base import BaseModel, ComponentSet
from mcaddon.core.file import ResourceFile
from .component import ParticleComponent


class BasicRenderParameters(BaseModel):
    material: str
    texture: str


class ParticleDescription(BaseDescription):
    basic_render_parameters: BasicRenderParameters


# TODO: Curves
class Curve(BaseModel):
    type: CurveType
    input: str
    horizontal_range: str
    nodes: List[float] = Field(default_factory=list)

    @field_validator("type", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return CurveType.parse(v)


@resourcepack("particles")
class Particle(ResourceFile):
    TYPE_ID = "particle_effect"
    format_version: str = "1.10.0"

    description: ParticleDescription = ParticleDescription(
        identifier="minecraft:explosion_emitter",
        basic_render_parameters=BasicRenderParameters(
            material="particle", texture="textures/particle/explosion"
        ),
    )
    components: ComponentSet[ParticleComponent] = Field(default_factory=ComponentSet)
    events: Dict[str, Any] = Field(default_factory=dict)
    curves: Dict[str, Curve] = Field(default_factory=dict)

    @property
    def id(self) -> str:
        return self.description.identifier
