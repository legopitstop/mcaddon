__all__ = ["EntityStalkAndPounceOnTargetComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import FilterTest
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityStalkAndPounceOnTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stalk_and_pounce_on_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.stalk_and_pounce_on_target"

    interest_time: float = 2
    leap_dist: Optional[float] = None
    leap_distance: float = 0.8
    leap_height: float = 0.9
    max_stalk_dist: float = 10
    pounce_max_dist: float = 5
    set_persistent: bool = False
    stalk_speed: float = 1.2
    strike_dist: float = 2
    stuck_blocks: Optional[FilterTest] = None
    stuck_time: float = 2
