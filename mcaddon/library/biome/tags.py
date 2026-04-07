__all__ = [
    "BiomeTagsComponent",
]

from typing import List, ClassVar
from pydantic import Field
from .component import BiomeComponent


@BiomeComponent.register
class BiomeTagsComponent(BiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_tags)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:tags"

    tags: List[str] = Field(default_factory=list)
