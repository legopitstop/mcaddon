__all__ = ["ClientBiomePrecipitationComponent"]

from typing import Optional, ClassVar
from .component import ClientBiomeComponent


@ClientBiomeComponent.register
class ClientBiomePrecipitationComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_precipitation)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:precipitation"

    ash: Optional[float] = None
    blue_spores: Optional[float] = None
    red_spores: Optional[float] = None
    white_ash: Optional[float] = None
