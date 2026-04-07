__all__ = [
    "BiomeClimateComponent",
]

from typing import Optional, ClassVar
from mcaddon.core import NumberRange
from .component import BiomeComponent


@BiomeComponent.register
class BiomeClimateComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_climate)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:climate"

    ash: Optional[float] = None
    blue_spores: Optional[float] = None
    downfall: Optional[float] = None
    red_spores: Optional[float] = None
    white_ash: Optional[float] = None
    temperature: Optional[float] = None
    snow_accumulation: Optional[NumberRange] = None
