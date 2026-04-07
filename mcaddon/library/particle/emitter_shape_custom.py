__all__ = ["EmitterShapeCustomComponent"]


from typing import List, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from .component import ParticleComponent


@ParticleComponent.register
class EmitterShapeCustomComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_shape_custom)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_shape_custom"

    offset: List[float | MolangExpr] = Field(default_factory=list)
    direction: List[float | MolangExpr] = Field(default_factory=list)
