__all__ = ["EntityVexCopyOwnerTargetComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityVexCopyOwnerTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_vex_copy_owner_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.vex_copy_owner_target"

    entity_types: List[EntityType] = Field(default_factory=list)
