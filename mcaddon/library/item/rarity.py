__all__ = [
    "ItemRarityComponent",
]

from typing import ClassVar
from mcaddon.core.base import ValueComponent
from mcaddon.library.constants import ItemRarity
from .component import ItemComponent


@ItemComponent.register
class ItemRarityComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_rarity)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:rarity"

    value: ItemRarity
