__all__ = ["ParticleLifetimeKillPlaneComponent"]

from typing import Tuple, ClassVar
from mcaddon.core.base import ValueComponent
from .component import ParticleComponent


@ParticleComponent.register
class ParticleLifetimeKillPlaneComponent(ValueComponent, ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_lifetime_kill-plane)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_kill_plane"

    value: Tuple[float, float, float, float]
