__all__ = ["EntityFindCoverComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityFindCoverComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_cover)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.find_cover"

    cooldown_time: float = 0
    speed_multiplier: float = 1
