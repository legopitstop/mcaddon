__all__ = ["EntityHurtByTargetComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityHurtByTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hurt_by_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.hurt_by_target"

    alert_same_type: bool = False
    entity_types: List[EntityType] | EntityType = Field(default_factory=list)
    hurt_owner: bool = False
