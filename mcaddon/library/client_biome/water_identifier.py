__all__ = ["ClientBiomeWaterIdentifierComponent"]

from .component import ClientBiomeComponent
from typing import ClassVar


@ClientBiomeComponent.register
class ClientBiomeWaterIdentifierComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_water_identifier)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:water_identifier"

    water_identifier: str
