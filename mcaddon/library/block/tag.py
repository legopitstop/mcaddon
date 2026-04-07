__all__ = [
    "BlockTagComponent",
]

from .component import BlockComponent


class BlockTagComponent(BlockComponent):
    def __hash__(self) -> int:
        return hash(self.tag)

    tag: str
    value: bool = True
