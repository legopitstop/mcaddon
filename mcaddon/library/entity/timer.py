__all__ = ["EntityTimerComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field

from mcaddon.core.base import NumberRange, BaseModel
from .event import EntityTriggerEvent
from .component import EntityComponent


class TimerChoice(BaseModel):
    weight: int
    value: int


@EntityComponent.register
class EntityTimerComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_timer)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:timer"

    looping: bool = True
    time: Optional[NumberRange | float] = 0
    time_down_event: Optional[EntityTriggerEvent] = None
    random_time_choices: List[TimerChoice] = Field(default_factory=list)
    randomInterval: bool = True
