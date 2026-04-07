__all__ = ["EntitySwimWithEntityComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntitySwimWithEntityComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_with_entity)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.swim_with_entity"

    catch_up_multiplier: float = 2.5
    catch_up_threshold: float = 12
    chance_to_stop: float = 0.0333
    entity_types: Optional[List[EntityType] | EntityType] = Field(default_factory=list)
    match_direction_threshold: float = 2
    search_range: float = 20
    speed_multiplier: float = 1.5
    state_check_interval: float = 0.5
    stop_distance: float = 5
    success_rate: float = 0.1
