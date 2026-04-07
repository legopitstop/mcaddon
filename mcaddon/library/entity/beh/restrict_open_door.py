__all__ = ["EntityRestrictOpenDoorComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRestrictOpenDoorComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_restrict_open_door)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.restrict_open_door"
