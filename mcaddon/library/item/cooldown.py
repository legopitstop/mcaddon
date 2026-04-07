__all__ = ["ItemCooldownComponent"]

from typing import ClassVar
from mcaddon.library.constants import ItemCooldownType
from .component import ItemComponent


@ItemComponent.register
class ItemCooldownComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_cooldown)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:cooldown"

    category: str
    duration: float
    type: ItemCooldownType = ItemCooldownType.USE
