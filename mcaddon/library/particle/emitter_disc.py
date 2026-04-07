__all__ = ["EmitterDiscComponent"]


from typing import List, ClassVar

from molang.dsl import MolangExpr
from pydantic import Field
from .component import ParticleComponent


@ParticleComponent.register
class EmitterDiscComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_disc)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_disc"

    plane_normal: str | List[float | MolangExpr]
    offset: List[float | MolangExpr] = Field(default_factory=list)
    radius: float | MolangExpr = 1
    surface_only: bool = False
    direction: str | List[float | MolangExpr]
