__all__ = ["EntityShareItemsComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityShareItemsComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_share_items)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.share_items"

    entity_types: List[EntityType] = Field(default_factory=list)
    goal_radius: float = 0.5
    max_dist: float = 0
    speed_multiplier: float = 1
