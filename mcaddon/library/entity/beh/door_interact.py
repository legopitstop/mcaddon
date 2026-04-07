__all__ = ["EntityDoorInteractComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityDoorInteractComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_door_interact)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.door_interact"
