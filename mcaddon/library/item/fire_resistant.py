__all__ = [
    "ItemFireResistantComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemFireResistantComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fire_resistant)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:fire_resistant"

    value: bool = True
