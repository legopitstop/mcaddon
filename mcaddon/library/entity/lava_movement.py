__all__ = ["EntityLavaMovementComponent"]

from typing import Optional, ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityLavaMovementComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_lava_movement)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:lava_movement"

    value: Optional[float] = None
