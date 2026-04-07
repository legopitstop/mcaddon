__all__ = ["EntityNearestPrioritizedAttackableTargetComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityNearestPrioritizedAttackableTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nearest_prioritized_attackable_target)
    """

    COMPONENT_ID: ClassVar[str] = (
        "minecraft:behavior.nearest_prioritized_attackable_target"
    )

    attack_interval: int = 0
    cooldown: float = 0
    entity_types: List[EntityType] = Field(default_factory=list)
    must_reach: bool = False
    must_see: bool = False
    must_see_forget_duration: float = 3
    persist_time: float = 0
    reselect_targets: bool = False
    scan_interval: int = 10
    set_persistent: bool = False
    target_search_height: float = -1
    within_radius: float = 0
