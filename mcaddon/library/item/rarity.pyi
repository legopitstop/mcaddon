from .component import ItemComponent
from mcaddon.core.base import ValueComponent
from mcaddon.library.constants import ItemRarity

__all__ = ["ItemRarityComponent"]

class ItemRarityComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_rarity)
    """

    value: ItemRarity
