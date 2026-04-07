__all__ = ["EntitySittableComponent"]

from typing import Optional, ClassVar
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntitySittableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_sittable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:sittable"

    sit_event: Optional[EntityTriggerEvent] = None
    stand_event: Optional[EntityTriggerEvent] = None
