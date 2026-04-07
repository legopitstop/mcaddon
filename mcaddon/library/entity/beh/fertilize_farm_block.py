__all__ = ["EntityFertilizeFarmBlockComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityFertilizeFarmBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_fertilize_farm_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.fertilize_farm_block"

    goal_radius: float = 1.5
    max_fertilizer_usage: int = 1
    search_cooldown_max_seconds: float = 8
    search_count: int = 9
    search_height: int = 1
    search_range: int = 1
    speed_multiplier: float = 0.5
