__all__ = ["EntityOnHurtComponent"]

from .event import EntityTriggerEvent
from typing import ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityOnHurtComponent(EntityComponent, EntityTriggerEvent):
    COMPONENT_ID: ClassVar[str] = "minecraft:on_hurt"
