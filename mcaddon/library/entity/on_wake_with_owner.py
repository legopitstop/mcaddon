__all__ = ["EntityOnWakeWithOwnerComponent"]

from .event import EntityTriggerEvent
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityOnWakeWithOwnerComponent(EntityComponent, EntityTriggerEvent):
    COMPONENT_ID: ClassVar[str] = "minecraft:on_wake_with_owner"
