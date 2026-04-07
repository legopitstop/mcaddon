__all__ = [
    "ItemDamageComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemDamageComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_damage)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:damage"

    value: int
