__all__ = ["ClientBiomeSkyColorComponent"]

from typing import List, ClassVar
from .component import ClientBiomeComponent


@ClientBiomeComponent.register
class ClientBiomeSkyColorComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_sky_color)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:sky_color"

    sky_color: str | List[float]
