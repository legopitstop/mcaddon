__all__ = ["EntityTargetWhenPushedComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityTargetWhenPushedComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_target_when_pushed)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.target_when_pushed"

    entity_types: List[EntityType] = Field(default_factory=list)
    percent_chance: float = 5.0
    priority: Optional[int] = None
