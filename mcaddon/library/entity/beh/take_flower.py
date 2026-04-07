__all__ = ["EntityTakeFlowerComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import Filter
from mcaddon.core.types import Vector3
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityTakeFlowerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_take_flower)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.take_flower"

    filters: Optional[Filter] = None
    max_head_rotation_y: float = 30
    max_rotation_x: float = 30
    max_wait_time: float = 20
    min_distance_to_target: float = 2
    min_wait_time: float = 4
    on_take_flower: Optional[EntityTriggerEvent] = None
    search_area: Vector3 = (6, 2, 6)
    speed_multiplier: float = 0.5
