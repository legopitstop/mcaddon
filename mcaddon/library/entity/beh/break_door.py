__all__ = ["EntityBreakDoorComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityBreakDoorComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_break_door)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.break_door"
