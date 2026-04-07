__all__ = ["EntityRaidGardenComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityRaidGardenComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_raid_garden)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.raid_garden"

    blocks: List[str] = Field(default_factory=list)
    eat_delay: int = 2
    full_delay: int = 100
    goal_radius: float = 0.5
    initial_eat_delay: int = 0
    max_to_eat: int = 6
    search_height: Optional[float] = None
    search_range: int = 0
    speed_multiplier: float = 1
