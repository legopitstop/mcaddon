__all__ = ["EntityLootComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityLootComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_loot)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:loot"

    table: str
