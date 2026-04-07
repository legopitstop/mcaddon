__all__ = ["EntityOnTargetAcquiredComponent"]

from .event import EntityTriggerEvent
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityOnTargetAcquiredComponent(EntityComponent, EntityTriggerEvent):
    COMPONENT_ID: ClassVar[str] = "minecraft:on_target_acquired"
