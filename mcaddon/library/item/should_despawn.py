__all__ = [
    "ItemShouldDespawnComponent",
]

from typing import ClassVar
from mcaddon import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemShouldDespawnComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_should_despawn)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:should_despawn"

    value: bool
