__all__ = ["EntityStayNearNoteblockComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityStayNearNoteblockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stay_near_noteblock)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.stay_near_noteblock"

    speed: int = 0
    start_distance: int = 0
    stop_distance: int = 0
