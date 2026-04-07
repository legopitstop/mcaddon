__all__ = ["EntityGroundOffsetComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityGroundOffsetComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ground_offset)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:ground_offset"

    value: float = 0
