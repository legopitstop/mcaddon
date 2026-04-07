__all__ = ["EntityFollowCaravanComponent"]

from typing import List, ClassVar
from pydantic import Field

from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityFollowCaravanComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_caravan)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.follow_caravan"

    entity_count: int = 1
    entity_types: List[EntityType] | EntityType = Field(default_factory=list)
    speed_multiplier: float = 1
