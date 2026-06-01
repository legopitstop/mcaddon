__all__ = ["EmitterLifetimeEventsComponent", "ParticleTravelDistanceEffect"]


from typing import Dict, List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import ParticleComponent


class ParticleTravelDistanceEffect(BaseModel):
    distance: float
    effects: List[str] = Field(default_factory=list)


@ParticleComponent.register
class EmitterLifetimeEventsComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_lifetime_events)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_lifetime_events"

    creation_event: List[str] | str
    expiration_event: List[str] | str = Field(default_factory=list)
    timeline: Dict[str, List[str] | str] = Field(default_factory=dict)
    travel_distance_events: Dict[str, List[str] | str] = Field(default_factory=dict)
    looping_travel_distance_events: List[ParticleTravelDistanceEffect] = Field(
        default_factory=list
    )
