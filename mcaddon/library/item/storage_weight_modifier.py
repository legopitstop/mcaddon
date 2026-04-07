__all__ = [
    "ItemStorageWeightModifierComponent",
]

from typing import ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemStorageWeightModifierComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_storage_weight_modifier)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:storage_weight_modifier"

    weight_in_storage_item: int = 4
