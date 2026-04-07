__all__ = ["EntityVibrationListenerComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityVibrationListenerComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vibration_listener)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:vibration_listener"
