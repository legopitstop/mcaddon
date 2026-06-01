__all__ = ["ClientBiomeAmbientSoundsComponent", "ClientBiomeAmbientSound"]

from typing import Optional, ClassVar
from .component import ClientBiomeComponent
from mcaddon.core.base import BaseModel


class ClientBiomeAmbientSound(BaseModel):
    asset: str
    chance: float


@ClientBiomeComponent.register
class ClientBiomeAmbientSoundsComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_ambient_sounds)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:ambient_sounds"

    addition: Optional[ClientBiomeAmbientSound | str] = None
    loop: Optional[str] = None
    mood: Optional[str] = None
    underwater_loop: Optional[str] = None
    underwater_addition: Optional[ClientBiomeAmbientSound | str] = None
