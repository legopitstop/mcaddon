__all__ = ["EntityExploreOutskirtsComponent"]

from mcaddon.core.types import Vector3
from typing import ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityExploreOutskirtsComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_explore_outskirts)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.explore_outskirts"

    dist_from_boundary: Vector3 = (5, 0, 5)
    explore_dist: float = 5
    max_travel_time: float = 60
    max_wait_time: float = 0
    min_dist_from_target: float = 2.2
    min_perimeter: float = 1
    min_wait_time: float = 3
    next_xz: int = 5
    next_y: int = 3
    speed_multiplier: float = 1
    timer_ratio: float = 2
