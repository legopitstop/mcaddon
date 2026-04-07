__all__ = ["EntityOpenDoorComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityOpenDoorComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_open_door)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.open_door"

    close_door_after: bool = True
