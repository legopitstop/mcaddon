__all__ = ["ClientBiomeAtmosphereIdentifierComponent"]

from .component import ClientBiomeComponent
from typing import ClassVar


@ClientBiomeComponent.register
class ClientBiomeAtmosphereIdentifierComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_atmosphere_identifier)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:atmosphere_identifier"

    atmosphere_identifier: str
