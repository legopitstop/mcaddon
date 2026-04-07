__all__ = ["EntityGrowsCropComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityGrowsCropComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_grows_crop)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:grows_crop"

    chance: float = 0
    charges: int = 10
