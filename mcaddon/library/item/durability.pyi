from .component import ItemComponent
from mcaddon.core.base import NumberRange

__all__ = ["ItemDurabilityComponent"]

class ItemDurabilityComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability)
    """

    max_durability: int
    damage_chance: NumberRange = ...
