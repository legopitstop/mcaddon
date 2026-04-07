__all__ = ["EntityDefendTrustedTargetComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
    EntityType,
)


@EntityComponent.register
class EntityDefendTrustedTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_defend_trusted_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.defend_trusted_target"
    aggro_sound: Optional[str] = None
    attack_interval: int = 0
    entity_types: List[EntityType] = Field(default_factory=list)
    must_see: bool = False
    must_see_forget_duration: float = 3
    on_defend_start: Optional[EntityTriggerEvent] = None
    sound_chance: Optional[float] = None
    within_radius: float = 0
