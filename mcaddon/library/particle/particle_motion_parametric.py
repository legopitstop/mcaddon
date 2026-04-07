__all__ = ["ParticleMotionParametricComponent"]


from typing import List, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from .component import ParticleComponent


@ParticleComponent.register
class ParticleMotionParametricComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_motion_parametric)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_motion_parametric"

    relative_position: List[float | MolangExpr] = Field(default_factory=list)
    direction: List[float | MolangExpr] = Field(default_factory=list)
    rotation: float | MolangExpr = 0
