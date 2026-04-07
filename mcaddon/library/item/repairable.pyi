from .component import ItemComponent
from mcaddon.core.base import BaseModel, ItemLike
from molang.dsl import MolangExpr

__all__ = ["ItemRepairableComponent", "RepairItem"]

class RepairItem(BaseModel):
    repair_amount: MolangExpr | float
    items: list[ItemLike] = ...

    def add(self, *item: ItemLike) -> "RepairItem": ...

class ItemRepairableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_repairable)
    """

    repair_items: list[RepairItem] = ...
    on_repaired: str | None = ...

    def add(self, *repair_item: RepairItem) -> "ItemRepairableComponent": ...
