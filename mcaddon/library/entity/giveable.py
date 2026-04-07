__all__ = ["EntityGiveableComponent", "GiveableTriggers"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .event import EntityTriggerEvent
from .component import EntityComponent


class GiveableTriggers(BaseModel):
    cooldown: Optional[float] = None
    items: Optional[List[str] | str] = Field(default_factory=list)
    on_give: Optional[EntityTriggerEvent] = None


@EntityComponent.register
class EntityGiveableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_giveable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:giveable"

    cooldown: float = 0
    items: List[str] = Field(default_factory=list)
    on_give: Optional[EntityTriggerEvent] = None
    triggers: Optional[GiveableTriggers] = None
