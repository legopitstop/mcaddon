__all__ = ["EntityAvoidMobTypeComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityAvoidMobTypeComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_avoid_mob_type)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.avoid_mob_type"

    avoid_mob_sound: Optional[str] = None
    avoid_target_xz: int = 16
    avoid_target_y: int = 7
    entity_types: Optional[List[EntityType] | EntityType] = Field(default_factory=list)
    ignore_visibility: bool = False
    max_dist: float = 3
    max_flee: float = 10
    on_escape_event: Optional[EntityTriggerEvent] = None
    probability_per_strength: float = 1
    remove_target: bool = False
    sound_interval: Optional[NumberRange] = None
    sprint_distance: float = 7
    sprint_speed_multiplier: float = 1
    walk_speed_multiplier: float = 1
