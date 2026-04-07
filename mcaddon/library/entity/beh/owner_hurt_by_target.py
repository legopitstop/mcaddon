__all__ = ["EntityOwnerHurtByTargetComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityOwnerHurtByTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_owner_hurt_by_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.owner_hurt_by_target"

    entity_types: List[EntityType] = Field(default_factory=list)
