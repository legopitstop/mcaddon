__all__ = ["ParticleAppearanceLightingComponent"]


from .component import ParticleComponent
from typing import ClassVar


@ParticleComponent.register
class ParticleAppearanceLightingComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_appearance_lighting)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_appearance_lighting"
