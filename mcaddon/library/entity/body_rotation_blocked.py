__all__ = ["EntityBodyRotationBlockedComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityBodyRotationBlockedComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_blocked)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:body_rotation_blocked"
