__all__ = ["EmitterRateSteadyComponent"]


from molang.dsl import MolangExpr
from typing import ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class EmitterRateSteadyComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_rate_steady)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_rate_steady"

    spawn_rate: float | MolangExpr = 1
    max_particles: float | MolangExpr = 50
