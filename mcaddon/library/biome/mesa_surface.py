__all__ = [
    "BiomeMesaSurfaceComponent",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BlockLike
from .component import BiomeComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use BiomeSurfaceBuilderComponent instead.")
@BiomeComponent.register
class BiomeMesaSurfaceComponent(BiomeComponent):
    """
    Use minecraft:surface_builder in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:mesa_surface"
    format_version = "<1.20.60"

    bryce_pillars: bool
    has_forest: bool
    sea_floor_depth: int
    clay_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    foundation_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    hard_clay_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    mid_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_floor_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    top_material: List[BlockLike] | BlockLike = Field(default_factory=list)
