__all__ = ["EntityUnderwaterMountBreathingComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityUnderwaterMountBreathingComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_underwater_mount_breathing)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:underwater_mount_breathing"
