from abc import ABC
from mcaddon.core.base import BaseComponent, BaseModel, Number

__all__ = ["BlockComponent", "BlockFilter"]

class BlockFilter(BaseModel):
    name: str | None
    states: dict[str, str | Number] | None
    tags: str | None

class BlockComponent(ABC, BaseComponent): ...
