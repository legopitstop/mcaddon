__all__ = ["BlockFormat"]

from typing import Dict, Any
from pydantic import Field
from mcaddon.core.file import NbtFile


class BlockFormat(NbtFile):
    name: str
    states: Dict[str, Any] = Field(default_factory=dict)
