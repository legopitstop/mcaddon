__all__ = ["ParticleLifetimeEventsComponent"]


from typing import Dict, List, ClassVar

from pydantic import Field
from .component import ParticleComponent


@ParticleComponent.register
class ParticleLifetimeEventsComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_lifetime_events)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_lifetime_events"

    creation_event: List[str] | str = Field(default_factory=list)
    expiration_event: List[str] | str = Field(default_factory=list)
    timeline: Dict[float, str | List[str]] = Field(default_factory=dict)
