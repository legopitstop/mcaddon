__all__ = ["EntityShareablesComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class SharableItem(BaseModel):
    admire: bool = False
    barter: bool = False
    consume_item: bool = False
    craft_into: Optional[str] = None
    item: Optional[str] = None
    max_amount: int = -1
    pickup_limit: int = -1
    pickup_only: bool = False
    priority: int = 0
    stored_in_inventory: bool = False
    surplus_amount: int = -1
    want_amount: int = -1


@EntityComponent.register
class EntityShareablesComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_shareables)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:shareables"

    all_items: bool = False
    all_items_max_amount: int = -1
    all_items_surplus_amount: int = -1
    all_items_want_amount: int = -1
    items: List[SharableItem] = Field(default_factory=list)
    singular_pickup: bool = False
