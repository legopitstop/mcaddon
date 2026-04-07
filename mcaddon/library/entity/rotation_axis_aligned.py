__all__ = ["EntityRotationAxisAlignedComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityRotationAxisAlignedComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rotation_axis_aligned)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:rotation_axis_aligned"
