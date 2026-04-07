__all__ = ["EmitterRateInstantComponent"]


from molang.dsl import MolangExpr
from typing import ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class EmitterRateInstantComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_rate_instant)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_rate_instant"

    num_particles: float | MolangExpr = 10
