__all__ = ["BlockEntityFormat"]

from typing import Optional
from mcaddon.core.file import NbtFile


class BlockEntityFormat(NbtFile):
    id: str
    isMoveable: bool
    x: int
    y: int
    z: int
    CustomName: Optional[str] = None
