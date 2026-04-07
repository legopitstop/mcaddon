__all__ = ["EntityRaidTriggerComponent"]

from typing import Optional, ClassVar
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntityRaidTriggerComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_raid_trigger)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:raid_trigger"

    triggered_event: Optional[EntityTriggerEvent] = None
