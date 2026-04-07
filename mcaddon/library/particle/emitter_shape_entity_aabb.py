__all__ = ["EmitterShapeEntityAABBComponent"]


from typing import List, ClassVar
from molang.dsl import MolangExpr
from .component import ParticleComponent


@ParticleComponent.register
class EmitterShapeEntityAABBComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_shape_entity-aabb)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_shape_entity_aabb"

    surface_only: bool = False
    direction: str | List[float | MolangExpr]
