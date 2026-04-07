__all__ = ["EntityUnderwaterMovementComponent"]

from typing import Optional, ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityUnderwaterMovementComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_underwater_movement)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:underwater_movement"

    value: Optional[float] = None
