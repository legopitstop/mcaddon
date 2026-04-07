__all__ = [
    "ItemUseDurationComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemUseDurationComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_duration)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:use_duration"

    value: float
