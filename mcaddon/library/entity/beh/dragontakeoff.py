__all__ = ["EntityDragontakeoffComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityDragontakeoffComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dragontakeoff)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.dragontakeoff"
