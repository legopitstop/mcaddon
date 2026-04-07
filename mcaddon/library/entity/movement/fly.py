__all__ = ["EntityMovementFlyComponent"]

from mcaddon.library.entity.component import EntityComponent
from typing import ClassVar
from .base import EntityBaseMovementComponent


@EntityComponent.register
class EntityMovementFlyComponent(EntityBaseMovementComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.fly)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movement.fly"

    speed_when_turning: float = 0.2
    start_speed: float = 0.1
