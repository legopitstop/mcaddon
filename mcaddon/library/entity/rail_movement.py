__all__ = ["EntityRailMovementComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityRailMovementComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rail_movement)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:rail_movement"

    max_speed: float = 0.4
