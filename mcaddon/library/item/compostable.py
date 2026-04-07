__all__ = [
    "ItemCompostableComponent",
]

from typing import ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemCompostableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_compostable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:compostable"

    composting_chance: int
