__all__ = [
    "BiomeOverworldGenerationRulesComponent",
]

from typing import List, Optional, Tuple, ClassVar
from pydantic import Field
from mcaddon.core.base import BlockLike
from .component import BiomeComponent


@BiomeComponent.register
class BiomeOverworldGenerationRulesComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_overworld_generation_rules)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:overworld_generation_rules"

    generate_for_climates: List[Tuple[str, int]] = Field(default_factory=list)
    hills_transformation: Optional[
        BlockLike | List[BlockLike | Tuple[BlockLike, int]]
    ] = None
    mutate_transformation: Optional[
        BlockLike | List[BlockLike | Tuple[BlockLike, int]]
    ] = None
    river_transformation: Optional[
        BlockLike | List[BlockLike | Tuple[BlockLike, int]]
    ] = None
    shore_transformation: Optional[
        BlockLike | List[BlockLike | Tuple[BlockLike, int]]
    ] = None
