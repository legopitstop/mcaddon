__all__ = [
    "BiomeReplaceBiomesComponent",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import BiomeComponent


class BiomeReplacement(BaseModel):
    amount: float
    dimension: str
    noise_frequency_scale: float
    targets: List[str] = Field(default_factory=list)


@BiomeComponent.register
class BiomeReplaceBiomesComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_replace_biomes)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:replace_biomes"

    replacements: List[BiomeReplacement] = Field(default_factory=list)
