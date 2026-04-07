__all__ = [
    "BiomeCreatureSpawnProbabilityComponent",
]

from .component import BiomeComponent
from typing import ClassVar


@BiomeComponent.register
class BiomeCreatureSpawnProbabilityComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_creature_spawn_probability)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:creature_spawn_probability"

    probability: float
