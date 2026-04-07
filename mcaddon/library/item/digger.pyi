from .component import ItemComponent
from mcaddon.core.base import BaseModel, BlockLike

__all__ = ["ItemDiggerComponent", "DestroySpeed"]

class DestroySpeed(BaseModel):
    block: BlockLike
    speed: int

class ItemDiggerComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_digger)
    """

    destroy_speeds: list[DestroySpeed] = ...
    use_efficiency: bool = ...

    def add(self, *destroy_speed: DestroySpeed) -> "ItemDiggerComponent": ...
