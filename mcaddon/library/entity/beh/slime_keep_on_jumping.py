__all__ = ["EntitySlimeKeepOnJumpingComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySlimeKeepOnJumpingComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_keep_on_jumping)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.slime_keep_on_jumping"

    speed_multiplier: float = 1
