__all__ = ["ItemFormat"]

from typing import List, Dict, Any
from pydantic import Field

from mcaddon.core.file import NbtFile
from .block import BlockFormat


class ItemFormat(NbtFile):
    Block: BlockFormat
    CanDestroy: List[str] = Field(default_factory=list)
    CanPlaceOn: List[str] = Field(default_factory=list)
    Count: int
    Damage: int
    Name: str
    tag: Dict[str, Any] = Field(default_factory=dict)
    WasPickedUp: bool
