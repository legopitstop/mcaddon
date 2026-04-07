__all__ = ["EntityTameableComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import ItemResult
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntityTameableComponent(EntityComponent):
    COMPONENT_ID: ClassVar[str] = "minecraft:tameable"

    probability: Optional[float] = None
    tame_items: List[str | ItemResult] | str = Field(default_factory=list)
    tame_event: Optional[EntityTriggerEvent] = None
