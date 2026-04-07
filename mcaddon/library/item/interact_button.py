__all__ = [
    "ItemInteractButtonComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemInteractButtonComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_interact_button)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:interact_button"

    value: str | bool
