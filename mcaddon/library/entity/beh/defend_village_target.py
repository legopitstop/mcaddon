__all__ = ["EntityDefendVillageTargetComponent"]

from typing import Optional, ClassVar, List

from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityDefendVillageTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_defend_village_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.defend_village_target"

    attack_chance: float = 0.05
    attack_owner: bool = False
    entity_types: Optional[EntityType | List[EntityType]] = Field(default_factory=list)
    must_reach: bool = False
    must_see: bool = False
    must_see_forget_duration: float = 3
    persist_time: float = 0
    within_radius: float = 0
