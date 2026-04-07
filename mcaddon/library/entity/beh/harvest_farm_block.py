__all__ = ["EntityHarvestFarmBlockComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityHarvestFarmBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_harvest_farm_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.harvest_farm_block"

    goal_radius: float = 1.5
    max_seconds_before_search: float = 1
    search_cooldown_max_seconds: float = 8
    search_count: int = 0
    search_height: int = 1
    search_range: int = 16
    seconds_until_new_task: float = 0.5
    speed_multiplier: float = 0.5
