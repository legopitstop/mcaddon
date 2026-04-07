__all__ = ["ParticleAppearanceTintingComponent", "ParticleColor"]


from typing import List, Dict, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.core.types import HexColor, RGBA
from .component import ParticleComponent

GRADIENT = List[float | MolangExpr | HexColor | RGBA] | Dict[str, RGBA]


class ParticleColor(BaseModel):
    interpolant: float | MolangExpr
    gradient: GRADIENT = Field(default_factory=list)


@ParticleComponent.register
class ParticleAppearanceTintingComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_appearance_tinting)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_appearance_tinting"

    color: ParticleColor | RGBA
