__all__ = [
    "ItemHoverTextColorComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemHoverTextColorComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hover_text_color)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:hover_text_color"

    value: str
