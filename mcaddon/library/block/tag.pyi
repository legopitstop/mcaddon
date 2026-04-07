from .component import BlockComponent

__all__ = ["BlockTagComponent"]

class BlockTagComponent(BlockComponent):
    def __hash__(self) -> int: ...
    tag: str
    value: bool
