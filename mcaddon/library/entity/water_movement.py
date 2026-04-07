__all__ = ["EntityWaterMovementComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityWaterMovementComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_water_movement)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:water_movement"

    drag_factor: float = 0.8
