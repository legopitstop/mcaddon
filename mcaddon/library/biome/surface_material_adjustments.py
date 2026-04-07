__all__ = [
    "BiomeSurfaceMaterialAdjustmentsComponent",
]

from typing import List, Optional, Tuple, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from mcaddon.core.base import BlockLike, NumberRange, BaseModel
from .component import BiomeComponent


class Materials(BaseModel):
    foundation_material: Optional[BlockLike] = None
    mid_material: Optional[BlockLike] = None
    sea_floor_material: Optional[BlockLike] = None
    sea_material: Optional[BlockLike] = None
    top_material: Optional[BlockLike] = None


class Adjustment(BaseModel):
    materials: Materials
    noise_range: NumberRange
    height_range: Optional[MolangExpr | Tuple[MolangExpr, MolangExpr]] = None
    noise_frequency_scale: Optional[float] = None


@BiomeComponent.register
class BiomeSurfaceMaterialAdjustmentsComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_surface_material_adjustments)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:surface_material_adjustments"

    adjustments: List[Adjustment] = Field(default_factory=list)
    foundation_material: Optional[BlockLike] = None
    mid_material: Optional[BlockLike] = None
    sea_floor_material: Optional[BlockLike] = None
    sea_material: Optional[BlockLike] = None
    top_material: Optional[BlockLike] = None
