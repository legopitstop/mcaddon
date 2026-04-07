__all__ = ["ClientBiomeBiomeMusicComponent"]

from typing import Optional, ClassVar
from .component import ClientBiomeComponent


@ClientBiomeComponent.register
class ClientBiomeBiomeMusicComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_biome_music)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:biome_music"

    music_definition: Optional[str] = None
    volume_multiplier: Optional[float] = None
    underwater_music: Optional[bool] = None
