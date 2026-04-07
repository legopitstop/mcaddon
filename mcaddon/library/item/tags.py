__all__ = [
    "ItemTagsComponent",
]

from typing import List, ClassVar
from pydantic import Field
from .component import ItemComponent


@ItemComponent.register
class ItemTagsComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_tags)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:tags"

    tags: List[str] = Field(default_factory=list)

    def add(self, *tag: str) -> "ItemTagsComponent":
        self.tags.extend(tag)
        return self

    def remove(self, tag: str) -> "ItemTagsComponent":
        self.tags.remove(tag)
        return self
