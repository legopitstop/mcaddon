__all__ = ["EmitterInitializationComponent"]

from typing import Optional, ClassVar
from molang.dsl import MolangExpr
from .component import ParticleComponent


@ParticleComponent.register
class EmitterInitializationComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_initialization)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_initialization"

    creation_expression: Optional[MolangExpr] = None
    per_update_expression: Optional[MolangExpr] = None
