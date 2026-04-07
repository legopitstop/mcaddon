__all__ = ["ClientBiomeFogAppearanceComponent"]

from .component import ClientBiomeComponent
from typing import ClassVar


@ClientBiomeComponent.register
class ClientBiomeFogAppearanceComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_fog_appearance)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:fog_appearance"

    fog_identifier: str
