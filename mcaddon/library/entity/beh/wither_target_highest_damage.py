__all__ = ["EntityWitherTargetHighestDamageComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityWitherTargetHighestDamageComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_wither_target_highest_damage)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.wither_target_highest_damage"

    entity_types: List[EntityType] = Field(default_factory=list)
