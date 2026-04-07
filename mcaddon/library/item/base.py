__all__ = ["Item", "ItemDescription"]

from typing import Optional, List
from pydantic import Field

from mcaddon.core.file import ResourceFile
from mcaddon.core.base import ComponentSet
from mcaddon.library.common import BaseDescription, MenuCategory
from mcaddon.library.pack import behaviorpack
from .component import ItemComponent


class ItemDescription(BaseDescription):
    menu_category: Optional[MenuCategory] = None
    category: Optional[str] = Field(default=None, deprecated=True)
    is_experimental: Optional[bool] = None


@behaviorpack("items")
class Item(ResourceFile):
    """
    Defines an item.
    """

    TYPE_ID = "minecraft:item"

    description: ItemDescription = ItemDescription(identifier="minecraft:air")
    components: ComponentSet[ItemComponent] = Field(default_factory=ComponentSet)

    @property
    def id(self) -> str:
        return self.description.identifier

    def get_tags(self) -> List[str]:
        com = self.components.get("tags")
        print(com)
        return []
