__all__ = [
    "BiomeVillageTypeComponent",
]

from typing import ClassVar
from mcaddon.library.constants import VillageType
from .component import BiomeComponent


@BiomeComponent.register
class BiomeVillageTypeComponent(BiomeComponent):
    """
    Determines the type of village for the Biome.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:village_type"
    type: VillageType
