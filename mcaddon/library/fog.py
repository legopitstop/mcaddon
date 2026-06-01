__all__ = [
    "FogSettings",
    "DistanceFog",
    "VolumetricFog",
    "FogItem",
    "TransitionFog",
    "InitFog",
    "FogDensity",
    "MediaCoefficients",
    "FogDensityItem",
    "MediaCoefficientsItem",
    "HenyeyGreensteinGItem",
    "HenyeyGreensteinG",
]

from pydantic import field_validator, Field
from typing import Optional, List


from mcaddon.core.file import ResourceFile
from mcaddon.core.base import BaseModel
from .pack import resourcepack
from .common import BaseDescription
from .constants import RenderDistanceType


class InitFog(BaseModel):
    render_distance_type: RenderDistanceType
    fog_start: Optional[float] = None
    fog_end: Optional[float] = None
    fog_color: Optional[str] = None

    @field_validator("render_distance_type", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return RenderDistanceType.parse(v)


class TransitionFog(BaseModel):
    init_fog: InitFog
    min_percent: Optional[float] = None
    mid_seconds: Optional[int] = None
    mid_percent: Optional[float] = None
    max_seconds: Optional[int] = None


class FogItem(BaseModel):
    render_distance_type: RenderDistanceType
    transition_fog: Optional[TransitionFog] = None
    fog_start: Optional[float] = None
    fog_end: Optional[float] = None
    fog_color: Optional[str] = None

    @field_validator("render_distance_type", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return RenderDistanceType.parse(v)


class DistanceFog(BaseModel):
    air: Optional[FogItem] = None
    lava: Optional[FogItem] = None
    lava_resistance: Optional[FogItem] = None
    powder_snow: Optional[FogItem] = None
    water: Optional[FogItem] = None
    weather: Optional[FogItem] = None


class FogDensityItem(BaseModel):
    max_density: float
    zero_density_height: float
    max_density_height: float


class FogDensity(BaseModel):
    air: Optional[FogDensityItem] = None
    lava: Optional[FogDensityItem] = None
    lava_resistance: Optional[FogDensityItem] = None
    water: Optional[FogDensityItem] = None
    weather: Optional[FogDensityItem] = None


class MediaCoefficientsItem(BaseModel):
    scattering: List[float] = Field(default_factory=list)
    absorption: List[float] = Field(default_factory=list)


class MediaCoefficients(BaseModel):
    air: Optional[MediaCoefficientsItem] = None
    cloud: Optional[MediaCoefficientsItem] = None
    water: Optional[MediaCoefficientsItem] = None


class HenyeyGreensteinGItem(BaseModel):
    henyey_greenstein_g: float


class HenyeyGreensteinG(BaseModel):
    air: Optional[HenyeyGreensteinGItem] = None


class VolumetricFog(BaseModel):
    density: FogDensity
    media_coefficients: MediaCoefficients
    henyey_greenstein_g: Optional[HenyeyGreensteinG] = None


@resourcepack("fogs")
class FogSettings(ResourceFile):
    TYPE_ID = "minecraft:fog_settings"
    format_version: str = "1.16.100"

    description: BaseDescription
    distance: Optional[DistanceFog] = None
    volumetric: Optional[VolumetricFog] = None

    @property
    def id(self) -> str:
        return self.description.identifier
