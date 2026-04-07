__all__ = ["ClientBiome"]

from pydantic import Field

from mcaddon.library.pack import resourcepack
from mcaddon.library.common import BaseDescription
from mcaddon.core.file import ResourceFile
from mcaddon.core.base import ComponentSet
from .component import ClientBiomeComponent


@resourcepack("biomes")
class ClientBiome(ResourceFile):
    TYPE_ID = "minecraft:client_biome"

    description: BaseDescription = BaseDescription(identifier="minecraft:plains")
    components: ComponentSet[ClientBiomeComponent] = Field(default_factory=ComponentSet)

    @property
    def id(self) -> str:
        return self.description.identifier
