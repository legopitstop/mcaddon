__all__ = [
    "ItemMaxStackSizeComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemMaxStackSizeComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_max_stack_size)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:max_stack_size"

    value: int = 64
