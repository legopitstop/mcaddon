__all__ = ["EntityFreeCameraControlledComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityFreeCameraControlledComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_free_camera_controlled)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:free_camera_controlled"

    strafe_speed_modifier: float
    backwards_movement_modifier: float
