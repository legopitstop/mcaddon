__all__ = ["EntityPeekComponent"]

from typing import Optional, ClassVar
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntityPeekComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_peek)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:peek"

    on_close: Optional[EntityTriggerEvent] = None
    on_open: Optional[EntityTriggerEvent] = None
    on_target_open: Optional[EntityTriggerEvent] = None
