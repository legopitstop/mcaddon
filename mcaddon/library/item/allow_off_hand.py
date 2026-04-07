__all__ = [
    "ItemAllowOffHandComponent",
]

from typing import ClassVar

from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemAllowOffHandComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_allow_off_hand)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:allow_off_hand"

    value: bool
