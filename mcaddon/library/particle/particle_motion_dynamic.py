__all__ = ["ParticleMotionDynamicComponent"]


from typing import List, ClassVar, Optional
from molang.dsl import MolangExpr
from pydantic import Field
from .component import ParticleComponent


@ParticleComponent.register
class ParticleMotionDynamicComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_motion_dynamic)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_motion_dynamic"

    linear_acceleration: List[float | MolangExpr] = Field(default_factory=list)
    linear_drag_coefficient: float | MolangExpr = 0
    rotation_acceleration: float | MolangExpr = 0
    rotation_drag_coefficient: float | MolangExpr = 0
    linear_drag: Optional[int] = None
