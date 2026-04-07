__all__ = ["ClientBiomeDryFoliageColorComponent"]

from typing import List, ClassVar
from .component import ClientBiomeComponent


@ClientBiomeComponent.register
class ClientBiomeDryFoliageColorComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_dry_foliage_color)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:dry_foliage_color"

    color: str | List[float]
