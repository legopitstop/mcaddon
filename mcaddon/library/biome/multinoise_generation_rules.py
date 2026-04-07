__all__ = [
    "BiomeMultinoiseGenerationRulesComponent",
]

from .component import BiomeComponent
from typing import ClassVar


@BiomeComponent.register
class BiomeMultinoiseGenerationRulesComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_multinoise_generation_rules)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:multinoise_generation_rules"

    weight: float
    target_altitude: float
    target_humidity: float
    target_temperature: float
    target_weirdness: float
