__all__ = ["EntityFireImmuneComponent"]

from mcaddon.core.base import ValueComponent
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityFireImmuneComponent(ValueComponent, EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_fire_immune)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:fire_immune"

    value: bool = True
