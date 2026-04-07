__all__ = ["ParticleLifetimeExpressionComponent"]


from molang.dsl import MolangExpr
from typing import ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class ParticleLifetimeExpressionComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_lifetime_expression)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_lifetime_expression"

    expiration_expression: float | MolangExpr = 0
    max_lifetime: float | MolangExpr
