__all__ = ["EntityScaredComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityScaredComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_scared)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.scared"

    sound_interval: int = 0
