__all__ = ["EmitterShapeSphereComponent"]


from typing import List, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from .component import ParticleComponent


@ParticleComponent.register
class EmitterShapeSphereComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_shape_sphere)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_shape_sphere"

    offset: List[float | MolangExpr] = Field(default_factory=list)
    radius: float | MolangExpr = 1
    surface_only: bool = False
    direction: str | List[float | MolangExpr]
