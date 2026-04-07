__all__ = [
    "BlockTagsComponent",
]

from .component import BlockComponent
from typing import Set, ClassVar
from pydantic import Field


@BlockComponent.register
class BlockTagsComponent(BlockComponent):
    COMPONENT_ID: ClassVar[str] = "minecraft:tags"

    tags: Set[str] = Field(default_factory=set)

    def add_tag(self, tag: str) -> "BlockTagsComponent":
        self.tags.add(tag)
        return self
