__all__ = ["EntityMovementJumpComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent
from .base import EntityBaseMovementComponent


@EntityComponent.register
class EntityMovementJumpComponent(EntityBaseMovementComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.jump)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movement.jump"

    jump_delay: Optional[NumberRange] = None
