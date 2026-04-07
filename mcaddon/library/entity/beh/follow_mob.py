__all__ = ["EntityFollowMobComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.library.filter import Filter
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityFollowMobComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_mob)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.follow_mob"

    filters: List[Filter] | Filter = Field(default_factory=list)
    preferred_actor_type: Optional[str] = None
    search_range: int = 0
    speed_multiplier: float = 1
    stop_distance: float = 2
    use_home_position_restriction: bool = True
