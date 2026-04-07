__all__ = ["EntitySuspectTrackingComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntitySuspectTrackingComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_suspect_tracking)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:suspect_tracking"
