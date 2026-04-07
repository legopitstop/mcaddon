__all__ = ["ParticleInitialSpeedComponent"]

from typing import Tuple, ClassVar
from molang.dsl import MolangExpr
from mcaddon.core.base import ValueComponent
from .component import ParticleComponent


@ParticleComponent.register
class ParticleInitialSpeedComponent(ValueComponent, ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_initial_speed)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_initial_speed"

    value: (
        float
        | MolangExpr
        | Tuple[float | MolangExpr, float | MolangExpr, float | MolangExpr]
    )
