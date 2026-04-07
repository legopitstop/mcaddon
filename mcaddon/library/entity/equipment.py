__all__ = ["EntityEquipmentComponent", "SlotDropChance"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class SlotDropChance(BaseModel):
    slot: str
    drop_chance: float


@EntityComponent.register
class EntityEquipmentComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equipment)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:equipment"

    slot_drop_chance: List[SlotDropChance] = Field(default_factory=list)
    table: Optional[str] = None
