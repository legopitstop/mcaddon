__all__ = ["EmitterLocalSpaceComponent"]

from typing import Optional, ClassVar
from .component import ParticleComponent


@ParticleComponent.register
class EmitterLocalSpaceComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_local_space)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_local_space"

    position: Optional[bool] = None
    rotation: Optional[bool] = None
    velocity: Optional[bool] = None
