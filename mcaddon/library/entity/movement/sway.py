__all__ = ["EntityMovementSwayComponent"]

from mcaddon.library.entity.component import EntityComponent
from typing import ClassVar
from .base import EntityBaseMovementComponent


@EntityComponent.register
class EntityMovementSwayComponent(EntityBaseMovementComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.sway)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movement.sway"

    sway_amplitude: float = 0.05
    sway_frequency: float = 0.5
