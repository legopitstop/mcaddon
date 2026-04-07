__all__ = [
    "ItemFuelComponent",
]

from typing import ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemFuelComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fuel)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:fuel"

    duration: int
