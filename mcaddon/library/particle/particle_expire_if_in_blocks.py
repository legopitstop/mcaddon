__all__ = ["ParticleExpireIfInBlocksComponent"]


from typing import List, ClassVar

from pydantic import Field
from mcaddon.core.base import ValueComponent
from .component import ParticleComponent


@ParticleComponent.register
class ParticleExpireIfInBlocksComponent(ValueComponent, ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_expire_if_in_blocks)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_expire_if_in_blocks"

    value: List[str] = Field(default_factory=list)
