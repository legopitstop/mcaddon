__all__ = [
    "ItemStackedByDataComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemStackedByDataComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_stacked_by_data)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:stacked_by_data"

    value: bool
