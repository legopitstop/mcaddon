__all__ = ["EntitySchedulerComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntitySchedulerComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scheduler)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:scheduler"

    max_delay_secs: Optional[float] = None
    min_delay_secs: Optional[float] = None
    scheduled_events: List[EntityTriggerEvent] = Field(default_factory=list)
