__all__ = [
    "BiomeSurfaceParametersComponent",
]

from mcaddon.core.base import BlockLike
from typing import ClassVar
from .component import BiomeComponent


@BiomeComponent.register
class BiomeSurfaceParametersComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_surface_parameters)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:surface_parameters"

    foundation_material: BlockLike
    mid_material: BlockLike
    sea_floor_material: BlockLike
    sea_material: BlockLike
    top_material: BlockLike
    sea_floor_depth: int
