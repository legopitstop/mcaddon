__all__ = ["EntityBodyRotationAxisAlignedComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityBodyRotationAxisAlignedComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_axis_aligned)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:body_rotation_axis_aligned"
