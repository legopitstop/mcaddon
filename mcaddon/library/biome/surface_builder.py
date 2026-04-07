__all__ = ["BiomeSurfaceBuilderComponent", "SurfaceBuilder"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseTypedModel, TypedModel
from mcaddon.core.base import BlockLike
from .component import BiomeComponent


class SurfaceBuilder(BaseTypedModel):
    pass


@SurfaceBuilder.register
class OverworldSurfaceBuilder(TypedModel):
    TYPE_ID = "minecraft:overworld"
    type: str = TYPE_ID

    sea_floor_depth: int
    foundation_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    mid_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_floor_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    top_material: List[BlockLike] | BlockLike = Field(default_factory=list)


@SurfaceBuilder.register
class CappedSurfaceBuilder(TypedModel):
    TYPE_ID = "minecraft:capped"
    type: str = TYPE_ID

    beach_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    ceiling_materials: List[BlockLike] | BlockLike = Field(default_factory=list)
    floor_materials: List[BlockLike] | BlockLike = Field(default_factory=list)
    foundation_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_material: List[BlockLike] | BlockLike = Field(default_factory=list)


@SurfaceBuilder.register
class FrozenOceanSurfaceBuilder(TypedModel):
    TYPE_ID = "minecraft:frozen_ocean"
    type: str = TYPE_ID

    sea_floor_depth: int
    foundation_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    mid_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_floor_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    top_material: List[BlockLike] | BlockLike = Field(default_factory=list)


@SurfaceBuilder.register
class MesaSurfaceBuilder(TypedModel):
    TYPE_ID = "minecraft:mesa"
    type: str = TYPE_ID

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


@SurfaceBuilder.register
class SwampSurfaceBuilder(TypedModel):
    TYPE_ID = "minecraft:swamp"
    type: str = TYPE_ID

    sea_floor_depth: int
    max_puddle_depth_below_sea_level: int
    foundation_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    mid_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_floor_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    sea_material: List[BlockLike] | BlockLike = Field(default_factory=list)
    top_material: List[BlockLike] | BlockLike = Field(default_factory=list)


@SurfaceBuilder.register
class TheEndSurfaceBuilder(TypedModel):
    TYPE_ID = "minecraft:the_end"
    type: str = TYPE_ID


@BiomeComponent.register
class BiomeSurfaceBuilderComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_surface_builder)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:surface_builder"

    builder: SurfaceBuilder
