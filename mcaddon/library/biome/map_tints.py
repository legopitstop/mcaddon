__all__ = [
    "BiomeMapTintsComponent",
]

from typing import Tuple, ClassVar
from mcaddon.core.base import BaseTypedModel, TypedModel
from mcaddon.core.types import HexColor
from .component import BiomeComponent


class GrassTint(BaseTypedModel):
    pass


@GrassTint.register
class TintGrassMap(TypedModel):
    TYPE_ID = "tint"
    type: str = TYPE_ID

    tint: HexColor


@GrassTint.register
class NoiseGrassMap(TypedModel):
    TYPE_ID = "noise"
    type: str = TYPE_ID


@BiomeComponent.register
class BiomeMapTintsComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_map_tints)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:map_tints"

    foliage: HexColor | Tuple[int, int, int]
    grass: GrassTint
