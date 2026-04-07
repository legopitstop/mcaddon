__all__ = ["EntityFollowParentComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityFollowParentComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_parent)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.follow_parent"

    speed_multiplier: float = 1
