__all__ = ["ClientBiomeComponent", "BiomeColor"]

from abc import ABC
from mcaddon.core.base import (
    BaseComponent,
    BaseModel,
)


class BiomeColor(BaseModel):
    color_map: str


class ClientBiomeComponent(ABC, BaseComponent):
    pass
