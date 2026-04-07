__all__ = ["EntityPlayerSaturationComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityAttributeComponent
from typing import ClassVar


@EntityComponent.register
class EntityPlayerSaturationComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.saturation)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:player.saturation"
