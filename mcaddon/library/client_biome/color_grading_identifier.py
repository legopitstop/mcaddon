__all__ = ["ClientBiomeColorGradingIdentifierComponent"]

from .component import ClientBiomeComponent
from typing import ClassVar


@ClientBiomeComponent.register
class ClientBiomeColorGradingIdentifierComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_color_grading_identifier)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:color_grading_identifier"

    color_grading_identifier: str
