__all__ = ["ParticleMotionCollisionComponent", "CollisionEvent"]

from molang.dsl import MolangExpr
from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import ParticleComponent


class CollisionEvent(BaseModel):
    event: str
    min_speed: float


@ParticleComponent.register
class ParticleMotionCollisionComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftparticle_motion_collision)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:particle_motion_collision"

    enabled: bool | MolangExpr = True
    collision_radius: float
    collision_drag: Optional[float] = None
    coefficient_of_restitution: Optional[float] = None
    expire_on_contact: Optional[bool] = None
    events: List[CollisionEvent] | CollisionEvent = Field(default_factory=list)
