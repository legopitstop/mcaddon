__all__ = [
    "ItemDurabilityComponent",
]

from typing import ClassVar
from mcaddon.core.base import NumberRange, NumberMinMax
from .component import ItemComponent


@ItemComponent.register
class ItemDurabilityComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:durability"

    max_durability: int
    damage_chance: NumberRange = NumberMinMax(min=0, max=100)
