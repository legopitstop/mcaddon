from .component import ItemComponent
from mcaddon.library.constants import EnchantableSlot

__all__ = ["ItemEnchantableComponent"]

class ItemEnchantableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_enchantable)
    """

    slot: EnchantableSlot
    value: int
