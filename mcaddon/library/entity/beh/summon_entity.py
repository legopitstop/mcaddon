__all__ = ["EntitySummonEntityComponent", "SummonChoices"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.filter import Filter
from mcaddon.library.constants import EventTarget
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from mcaddon.core.types import HexColor


class SummonSequence(BaseModel):
    base_delay: float = 0
    delay_per_summon: float = 0
    entity_lifespan: float = -1
    entity_type: Optional[str] = None
    num_entities_spawned: int = 1
    shape: str = "line"
    size: float = 1
    sound_event: Optional[str] = None
    summon_cap: int = 0
    summon_cap_radius: float = 0
    summon_event: Optional[str] = None
    target: EventTarget = EventTarget.SELF


class SummonChoices(BaseModel):
    cast_duration: Optional[float] = None
    cooldown_time: float = 0
    do_casting: bool = True
    filters: Optional[Filter] = None
    max_activation_range: float = 32
    min_activation_range: float = 1
    particle_color: int | HexColor = 0
    sequence: List[SummonSequence] = Field(default_factory=list)
    start_sound_event: Optional[str] = None
    weight: float = 0


@EntityComponent.register
class EntitySummonEntityComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_summon_entity)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.summon_entity"

    summon_choices: List[SummonChoices] = Field(default_factory=list)
