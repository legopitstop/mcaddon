__all__ = ["EntityDryingOutTimerComponent"]

from .component import EntityComponent
from typing import ClassVar
from .event import EntityTriggerEvent


@EntityComponent.register
class EntityDryingOutTimerComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_drying_out_timer)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:drying_out_timer"

    dried_out_event: EntityTriggerEvent
    recover_after_dried_out_event: EntityTriggerEvent
    stopped_drying_out_event: EntityTriggerEvent
    total_time: float = 0
    water_bottle_refill_time: float = 0
