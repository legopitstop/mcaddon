__all__ = ["EntityEmergeComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityEmergeComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_emerge)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.emerge"

    cooldown_time: float = 0.5
    duration: float = 5
    on_done: Optional[EntityTriggerEvent] = None
