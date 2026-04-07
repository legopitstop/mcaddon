__all__ = [
    "ItemDiggerComponent",
    "DestroySpeed",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, BlockLike
from .component import ItemComponent


class DestroySpeed(BaseModel):
    block: BlockLike
    speed: int


@ItemComponent.register
class ItemDiggerComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_digger)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:digger"

    destroy_speeds: List[DestroySpeed] = Field(default_factory=list)
    use_efficiency: bool = False

    def add(self, *destroy_speed: DestroySpeed) -> "ItemDiggerComponent":
        self.destroy_speeds.extend(destroy_speed)
        return self
