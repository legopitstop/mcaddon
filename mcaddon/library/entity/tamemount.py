__all__ = ["EntityTamemountComponent", "AutoRejectItem", "TamemountFeedItem"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .event import EntityTriggerEvent
from .component import EntityComponent


class AutoRejectItem(BaseModel):
    item: str


class TamemountFeedItem(BaseModel):
    item: str
    temper_mod: int = 0


@EntityComponent.register
class EntityTamemountComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tamemount)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:tamemount"

    attempt_temper_mod: int = 5
    auto_reject_items: List[AutoRejectItem] = Field(default_factory=list)
    autoRejectItems: List[AutoRejectItem] = Field(default_factory=list)
    feed_items: List[TamemountFeedItem] = Field(default_factory=list)
    feed_text: Optional[str] = None
    max_temper: int = 100
    min_temper: int = 0
    ride_text: Optional[str] = None
    tame_event: Optional[EntityTriggerEvent] = None
