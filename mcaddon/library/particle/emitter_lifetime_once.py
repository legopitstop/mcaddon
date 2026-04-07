__all__ = ["EmitterLifetimeOnceComponent"]


from molang.dsl import MolangExpr
from typing import ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class EmitterLifetimeOnceComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_lifetime_once)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_lifetime_once"

    active_time: float | MolangExpr = 10
