__all__ = ["EntityEquippableComponent", "EquippableSlot"]

from typing import List, Optional, ClassVar
from pydantic import Field

from mcaddon.core.base import BaseModel
from .event import EntityTriggerEvent
from .component import EntityComponent


class EquippableSlot(BaseModel):
    accepted_items: List[str] = Field(default_factory=list)
    interact_text: Optional[str] = None
    item: str
    on_equip: Optional[EntityTriggerEvent] = None
    on_unequip: Optional[EntityTriggerEvent] = None
    slot: int


@EntityComponent.register
class EntityEquippableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equippable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:equippable"

    slots: List[EquippableSlot] = Field(default_factory=list)
