__all__ = ["EmitterShapeBoxComponent"]


from typing import List, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from .component import ParticleComponent


@ParticleComponent.register
class EmitterShapeBoxComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_shape_box)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_shape_box"

    offset: List[float | MolangExpr] = Field(default_factory=list)
    half_dimensions: List[float | MolangExpr] = Field(default_factory=list)
    surface_only: bool = False
    direction: str | List[float | MolangExpr]
