__all__ = ["EntityEquipItemComponent", "EquipItem"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class EquipItem(BaseModel):
    item: str


@EntityComponent.register
class EntityEquipItemComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equip_item)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:equip_item"

    excluded_items: List[EquipItem] = Field(default_factory=list)
    can_wear_armor: Optional[bool] = None
