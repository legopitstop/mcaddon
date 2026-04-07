__all__ = ["EmitterLifetimeExpressionComponent"]


from molang.dsl import MolangExpr
from typing import ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class EmitterLifetimeExpressionComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_lifetime_expression)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_lifetime_expression"

    activation_expression: float | MolangExpr = 10
    expiration_expression: float | MolangExpr = 0
