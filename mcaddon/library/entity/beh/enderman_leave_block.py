__all__ = ["EntityEndermanLeaveBlockComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityEndermanLeaveBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_enderman_leave_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.enderman_leave_block"
