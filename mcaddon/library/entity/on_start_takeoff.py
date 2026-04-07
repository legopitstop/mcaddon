__all__ = ["EntityOnStartTakeoffComponent"]

from .event import EntityTriggerEvent
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityOnStartTakeoffComponent(EntityComponent, EntityTriggerEvent):
    COMPONENT_ID: ClassVar[str] = "minecraft:on_start_takeoff"
