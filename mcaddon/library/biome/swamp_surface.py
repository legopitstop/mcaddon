__all__ = [
    "BiomeSwampSurfaceComponent",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BlockLike
from .component import BiomeComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use BiomeSurfaceBuilderComponent instead.")
@BiomeComponent.register
class BiomeSwampSurfaceComponent(BiomeComponent):
    """
    Use minecraft:surface_builder in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:swamp_surface"
    format_version = "<1.20.60"

    sea_floor_depth: int
    foundation_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    mid_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_floor_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    top_material: List[BlockLike] | BlockLike = Field(default_factory=list)
