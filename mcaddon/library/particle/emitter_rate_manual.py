__all__ = ["EmitterRateManualComponent"]


from molang.dsl import MolangExpr
from typing import ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class EmitterRateManualComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_rate_manual)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_rate_manual"

    max_particles: float | MolangExpr = 50
