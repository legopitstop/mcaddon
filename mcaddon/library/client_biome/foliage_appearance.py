__all__ = ["ClientBiomeFoliageAppearanceComponent"]

from .component import ClientBiomeComponent, BiomeColor
from typing import ClassVar


@ClientBiomeComponent.register
class ClientBiomeFoliageAppearanceComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_foliage_appearance)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:foliage_appearance"

    color: str | BiomeColor
