__all__ = [
    "BiomeHumidityComponent",
]

from .component import BiomeComponent
from typing import ClassVar


@BiomeComponent.register
class BiomeHumidityComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_humidity)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:humidity"

    is_humid: bool
