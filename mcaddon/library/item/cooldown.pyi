from .component import ItemComponent
from mcaddon.library.constants import ItemCooldownType

__all__ = ["ItemCooldownComponent"]

class ItemCooldownComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_cooldown)
    """

    category: str
    duration: float
    type: ItemCooldownType = ...
