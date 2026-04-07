__all__ = [
    "ItemLiquidClippedComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemLiquidClippedComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_liquid_clipped)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:liquid_clipped"

    value: bool
