__all__ = ["EntityDolphinMovementComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityDolphinMovementComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dolphin_movement)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:dolphin_movement"
