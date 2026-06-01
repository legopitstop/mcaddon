__all__ = ["ItemShooterComponent", "ItemAmmunition"]

from typing import List, ClassVar

from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import ItemComponent


class ItemAmmunition(BaseModel):
    item: str
    search_inventory: bool = False
    use_in_creative: bool = False
    use_offhand: bool = False


@ItemComponent.register
class ItemShooterComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_shooter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:shooter"

    charge_on_draw: bool = False
    max_draw_duration: float = 0
    scale_power_by_draw_duration: bool = False
    ammunition: List[ItemAmmunition] = Field(default_factory=list)
