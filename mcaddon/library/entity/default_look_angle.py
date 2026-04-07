__all__ = ["EntityDefaultLookAngleComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityDefaultLookAngleComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_default_look_angle)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:default_look_angle"

    value: float = 0
