__all__ = ["EntityVibrationDamperComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityVibrationDamperComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vibration_damper)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:vibration_damper"
