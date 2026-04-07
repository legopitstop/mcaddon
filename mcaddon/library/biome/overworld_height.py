__all__ = [
    "BiomeOverworldHeightComponent",
]

from typing import List, Optional, ClassVar
from .component import BiomeComponent


@BiomeComponent.register
class BiomeOverworldHeightComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_overworld_height)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:overworld_height"

    noise_type: Optional[str] = None
    noise_params: Optional[List[float]] = None
