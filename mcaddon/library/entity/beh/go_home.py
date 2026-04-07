__all__ = ["EntityGoHomeComponent"]

from typing import Optional, List, ClassVar
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityGoHomeComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_go_home)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.go_home"

    calculate_new_path_radius: float = 2
    goal_radius: float = 0.5
    interval: int = 120
    on_failed: Optional[EntityTriggerEvent | List[EntityTriggerEvent]] = None
    on_home: Optional[EntityTriggerEvent | List[EntityTriggerEvent]] = None
    speed_multiplier: float = 1
