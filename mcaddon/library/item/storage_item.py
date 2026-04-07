__all__ = [
    "ItemStorageItemComponent",
]

from typing import List, Optional, ClassVar
from pydantic import Field
from .component import ItemComponent


@ItemComponent.register
class ItemStorageItemComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_storage_item)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:storage_item"

    allow_nested_storage_items: bool = True
    max_slots: int = 64
    max_weight_limit: Optional[float] = None
    weight_in_storage_item: Optional[float] = None
    allowed_items: List[str] = Field(default_factory=list)
    banned_items: List[str] = Field(default_factory=list)

    def banned(self, *item: str) -> "ItemStorageItemComponent":
        self.banned_items.extend(item)
        return self

    def allowed(self, *item: str) -> "ItemStorageItemComponent":
        self.allowed_items.extend(item)
        return self
