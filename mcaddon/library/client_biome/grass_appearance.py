__all__ = ["ClientBiomeGrassAppearanceComponent"]

from typing import Optional, ClassVar
from .component import ClientBiomeComponent, BiomeColor


@ClientBiomeComponent.register
class ClientBiomeGrassAppearanceComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_grass_appearance)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:grass_appearance"

    color: Optional[str | BiomeColor] = None
    grass_is_shaded: Optional[bool] = None
