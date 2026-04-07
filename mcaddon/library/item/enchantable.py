__all__ = ["ItemEnchantableComponent"]

from typing import ClassVar
from mcaddon.library.constants import EnchantableSlot
from .component import ItemComponent


@ItemComponent.register
class ItemEnchantableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_enchantable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:enchantable"

    slot: EnchantableSlot
    value: int
