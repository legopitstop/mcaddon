__all__ = [
    "ItemHandEquippedComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemHandEquippedComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hand_equipped)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:hand_equipped"

    value: bool = True
