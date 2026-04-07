__all__ = [
    "ItemBlockPlacerComponent",
]

from typing import ClassVar, List
from pydantic import Field

from mcaddon.core.base import BlockLike
from .component import ItemComponent


@ItemComponent.register
class ItemBlockPlacerComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_block_placer)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:block_placer"

    block: str
    replace_block_item: bool = False
    use_on: List[BlockLike] | BlockLike = Field(default_factory=list)
