__all__ = [
    "ItemDiggerComponent",
    "ItemDestroySpeed",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, BlockLike
from .component import ItemComponent


class ItemDestroySpeed(BaseModel):
    block: BlockLike
    speed: int


@ItemComponent.register
class ItemDiggerComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_digger)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:digger"

    destroy_speeds: List[ItemDestroySpeed] = Field(default_factory=list)
    use_efficiency: bool = False

    def add(self, *destroy_speed: ItemDestroySpeed) -> "ItemDiggerComponent":
        self.destroy_speeds.extend(destroy_speed)
        return self
