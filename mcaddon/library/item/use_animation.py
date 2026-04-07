__all__ = [
    "ItemUseAnimationComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemUseAnimationComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_animation)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:use_animation"

    value: str
