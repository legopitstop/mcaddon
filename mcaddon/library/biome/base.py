__all__ = ["Biome"]

from pydantic import Field

from mcaddon.library.pack import behaviorpack
from mcaddon.library.common import BaseDescription
from mcaddon.core.file import ResourceFile
from mcaddon.core.base import ComponentSet
from .component import BiomeComponent


@behaviorpack("biomes")
class Biome(ResourceFile):
    TYPE_ID = "minecraft:biome"

    description: BaseDescription = BaseDescription(identifier="minecraft:plains")
    components: ComponentSet[BiomeComponent] = Field(default_factory=ComponentSet)

    @property
    def id(self) -> str:
        return self.description.identifier
