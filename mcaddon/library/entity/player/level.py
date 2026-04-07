__all__ = ["EntityPlayerLevelComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityAttributeComponent
from typing import ClassVar


@EntityComponent.register
class EntityPlayerLevelComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.level)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:player.level"
