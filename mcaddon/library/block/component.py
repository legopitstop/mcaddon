__all__ = [
    "BlockComponent",
    "BlockFilter",
]

from typing import Dict, Optional
from abc import ABC
from mcaddon.core.base import (
    BaseComponent,
    BaseModel,
    Number,
)


class BlockFilter(BaseModel):
    name: Optional[str] = None
    states: Optional[Dict[str, str | Number]] = None
    tags: Optional[str] = None


class BlockComponent(ABC, BaseComponent):
    pass
