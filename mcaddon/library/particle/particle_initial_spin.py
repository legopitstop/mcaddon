__all__ = ["ParticleInitialSpinComponent"]


from molang.dsl import MolangExpr
from typing import ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class ParticleInitialSpinComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_initial_spin)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_initial_spin"

    rotation: float | MolangExpr = 0
    rotation_rate: float | MolangExpr = 0
