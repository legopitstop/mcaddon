__all__ = ["EntityWorkComposterComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityWorkComposterComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_work_composter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.work_composter"

    active_time: int = 0
    block_interaction_max: int = 1
    can_empty_composter: bool = True
    can_fill_composter: bool = True
    can_work_in_rain: bool = False
    goal_cooldown: int = 0
    items_per_use_max: int = 20
    min_item_count: int = 10
    on_arrival: Optional[EntityTriggerEvent] = None
    speed_multiplier: float = 0.5
    use_block_max: int = 200
    use_block_min: int = 100
    work_in_rain_tolerance: int = -1
