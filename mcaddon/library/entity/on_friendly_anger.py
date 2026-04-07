__all__ = ["EntityOnFriendlyAngerComponent"]

from .event import EntityTriggerEvent
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityOnFriendlyAngerComponent(EntityComponent, EntityTriggerEvent):
    COMPONENT_ID: ClassVar[str] = "minecraft:on_friendly_anger"
