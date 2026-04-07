__all__ = ["EmitterShapePointComponent"]


from typing import List, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from .component import ParticleComponent


@ParticleComponent.register
class EmitterShapePointComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_shape_point)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_shape_point"

    offset: List[float | MolangExpr] = Field(default_factory=list)
    direction: List[float | MolangExpr] = Field(default_factory=list)
