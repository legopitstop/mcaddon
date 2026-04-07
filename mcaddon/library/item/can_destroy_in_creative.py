__all__ = [
    "ItemCanDestroyInCreativeComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemCanDestroyInCreativeComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_can_destroy_in_creative)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:can_destroy_in_creative"

    value: bool
