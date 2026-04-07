__all__ = [
    "ItemDisplayNameComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemDisplayNameComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_display_name)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:display_name"

    value: str
