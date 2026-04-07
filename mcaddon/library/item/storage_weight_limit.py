__all__ = [
    "ItemStorageWeightLimitComponent",
]

from typing import ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemStorageWeightLimitComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_storage_weight_limit)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:storage_weight_limit"

    max_weight_limit: int = 64
