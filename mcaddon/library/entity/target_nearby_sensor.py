__all__ = ["EntityTargetNearbySensorComponent"]

from typing import Optional, ClassVar
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntityTargetNearbySensorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_target_nearby_sensor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:target_nearby_sensor"

    inside_range: float = 1
    must_see: bool = False
    on_inside_range: Optional[EntityTriggerEvent] = None
    on_outside_range: Optional[EntityTriggerEvent] = None
    on_vision_lost_inside_range: Optional[EntityTriggerEvent] = None
    outside_range: float = 5
