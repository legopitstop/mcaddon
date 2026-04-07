__all__ = ["ClientBiomeWaterAppearanceComponent"]

from typing import List, Optional, ClassVar
from .component import ClientBiomeComponent


@ClientBiomeComponent.register
class ClientBiomeWaterAppearanceComponent(ClientBiomeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_water_appearance)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:water_appearance"

    surface_color: str | List[float]
    surface_opacity: Optional[float] = None
