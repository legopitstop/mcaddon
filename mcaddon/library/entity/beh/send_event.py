__all__ = ["EntitySendEventComponent", "SendEventSequence", "SendEventChoices"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.filter import Filter
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


class SendEventSequence(BaseModel):
    base_delay: float = 0
    event: Optional[EntityTriggerEvent | str] = None
    sound_event: Optional[str] = None


class SendEventChoices(BaseModel):
    cast_duration: Optional[float] = None
    cooldown_time: Optional[float] = None
    filters: Optional[Filter] = None
    max_activation_range: Optional[float] = None
    min_activation_range: Optional[float] = None
    particle_color: Optional[str] = None
    sequence: List[SendEventSequence] = Field(default_factory=list)
    start_sound_event: Optional[str] = None
    weight: Optional[float] = None


@EntityComponent.register
class EntitySendEventComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_send_event)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.send_event"

    cast_duration: Optional[float] = None
    event_choices: List[SendEventChoices] = Field(default_factory=list)
    look_at_target: bool = True
    sequence: List[SendEventSequence] = Field(default_factory=list)
