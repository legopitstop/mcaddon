__all__ = ["EntityPlayerExperienceComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityAttributeComponent
from typing import ClassVar


@EntityComponent.register
class EntityPlayerExperienceComponent(EntityAttributeComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.experience)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:player.experience"
