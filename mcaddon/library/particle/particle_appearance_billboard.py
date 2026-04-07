__all__ = [
    "ParticleAppearanceBillboardComponent",
    "ParticleFlipbook",
    "ParticleUV",
    "BillboardDirection",
]


from typing import List, Tuple, Optional, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import BillboardDirectionMode, CameraFacingMode
from .component import ParticleComponent


class ParticleFlipbook(BaseModel):
    base_UV: Tuple[float | MolangExpr, float | MolangExpr]
    size_UV: Tuple[float | MolangExpr, float | MolangExpr]
    step_UV: Tuple[float | MolangExpr, float | MolangExpr]
    frames_per_second: Optional[float] = None
    max_frame: float | MolangExpr
    stretch_to_lifetime: Optional[bool] = None
    loop: Optional[bool] = None


class ParticleUV(BaseModel):
    texture_width: int
    texture_height: int
    uv: List[float | MolangExpr] = Field(default_factory=list)
    uv_size: List[float | MolangExpr] = Field(default_factory=list)
    flipbook: Optional[ParticleFlipbook] = None


class BillboardDirection(BaseModel):
    mode: BillboardDirectionMode
    min_speed_threshold: Optional[float] = None
    custom_direction: Optional[
        Tuple[float | MolangExpr, float | MolangExpr, float | MolangExpr]
    ] = None


@ParticleComponent.register
class ParticleAppearanceBillboardComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_appearance_billboard)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_appearance_billboard"

    size: Tuple[float | MolangExpr, float | MolangExpr]
    uv: Optional[ParticleUV] = None
    face_camera_mode: Optional[CameraFacingMode] = None
    facing_camera_mode: Optional[CameraFacingMode] = None
    direction: Optional[BillboardDirection] = None
