__all__ = ["EntityVerticalMovementActionComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityVerticalMovementActionComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vertical_movement_action)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:vertical_movement_action"

    vertical_velocity: float
