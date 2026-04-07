from .component import BlockComponent
from typing import Set

__all__ = ["BlockTagsComponent"]

class BlockTagsComponent(BlockComponent):
    tags: Set[str] = ...

    def add_tag(self, tag: str) -> "BlockTagsComponent": ...
