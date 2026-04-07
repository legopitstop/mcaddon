__all__ = ["EmitterLifetimeLoopingComponent"]


from molang.dsl import MolangExpr
from typing import ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class EmitterLifetimeLoopingComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_lifetime_looping)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_lifetime_looping"

    active_time: float | MolangExpr = 10
    sleep_time: float | MolangExpr = 0
