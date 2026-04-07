__all__ = [
    "BiomeCappedSurfaceComponent",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BlockLike
from .component import BiomeComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use BiomeSurfaceBuilderComponent instead.")
@BiomeComponent.register
class BiomeCappedSurfaceComponent(BiomeComponent):
    """
    Use minecraft:surface_builder in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:capped_surface"
    format_version = "<1.20.60"

    beach_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    ceiling_materials: List[BlockLike] | BlockLike = Field(default_factory=list)
    floor_materials: List[BlockLike] | BlockLike = Field(default_factory=list)
    foundation_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_material: List[BlockLike] | BlockLike = Field(default_factory=list)
