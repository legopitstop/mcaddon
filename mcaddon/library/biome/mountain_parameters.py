__all__ = ["BiomeMountainParametersComponent", "SteepMaterialAdjustment", "TopSlide"]

from typing import Optional, ClassVar
from mcaddon.core.base import BlockLike, BaseModel
from .component import BiomeComponent


class SteepMaterialAdjustment(BaseModel):
    north_slopes: Optional[bool] = None
    south_slopes: Optional[bool] = None
    east_slopes: Optional[bool] = None
    west_slopes: Optional[bool] = None
    material: BlockLike


class TopSlide(BaseModel):
    enabled: bool


@BiomeComponent.register
class BiomeMountainParametersComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_mountain_parameters)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:mountain_parameters"

    north_slopes: Optional[bool] = None
    south_slopes: Optional[bool] = None
    east_slopes: Optional[bool] = None
    west_slopes: Optional[bool] = None
    material: Optional[BlockLike] = None
    top_slide: Optional[TopSlide] = None
    steep_material_adjustment: Optional[SteepMaterialAdjustment] = None
