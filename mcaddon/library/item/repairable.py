__all__ = [
    "ItemRepairableComponent",
    "RepairItem",
]

from typing import List, Optional, ClassVar

from molang.dsl import MolangExpr
from pydantic import Field
from mcaddon.core.base import BaseModel, ItemLike
from .component import ItemComponent


class RepairItem(BaseModel):
    repair_amount: MolangExpr | float
    items: List[ItemLike] = Field(default_factory=list)

    def add(self, *item: ItemLike) -> "RepairItem":
        self.items.extend(item)
        return self


@ItemComponent.register
class ItemRepairableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_repairable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:repairable"

    repair_items: List[RepairItem] = Field(default_factory=list)
    on_repaired: Optional[str] = Field(deprecated=True, default=None)

    def add(self, *repair_item: RepairItem) -> "ItemRepairableComponent":
        self.repair_items.extend(repair_item)
        return self
