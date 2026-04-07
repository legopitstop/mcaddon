__all__ = ["ClientBiomeLightingIdentifierComponent"]

from .component import ClientBiomeComponent
from typing import ClassVar


@ClientBiomeComponent.register
class ClientBiomeLightingIdentifierComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_lighting_identifier)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:lighting_identifier"

    lighting_identifier: str
