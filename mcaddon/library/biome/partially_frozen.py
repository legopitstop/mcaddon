__all__ = [
    "BiomePartiallyFrozenComponent",
]

from .component import BiomeComponent
from typing import ClassVar


@BiomeComponent.register
class BiomePartiallyFrozenComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_partially_frozen)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:partially_frozen"
