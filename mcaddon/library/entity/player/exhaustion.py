__all__ = ["EntityPlayerExhaustionComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityAttributeComponent
from typing import ClassVar


@EntityComponent.register
class EntityPlayerExhaustionComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.exhaustion)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:player.exhaustion"
