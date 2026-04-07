__all__ = ["EntityMovementGlideComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent
from .base import EntityBaseMovementComponent


@EntityComponent.register
class EntityMovementGlideComponent(EntityBaseMovementComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.glide)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movement.glide"

    speed_when_turning: float = 0.2
    start_speed: Optional[float] = None
