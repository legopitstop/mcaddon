__all__ = ["ParticleInitializationComponent"]

from molang.dsl import MolangExpr
from typing import Optional, ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class ParticleInitializationComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_initialization)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_initialization"

    per_update_expression: Optional[MolangExpr] = None
    per_render_expression: Optional[MolangExpr] = None
