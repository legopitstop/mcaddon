from .component import ItemComponent
from mcaddon.core.base import BlockLike

__all__ = ["ItemBlockPlacerComponent"]

class ItemBlockPlacerComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_block_placer)
    """

    block: str
    replace_block_item: bool = ...
    use_on: list[BlockLike] | BlockLike = ...
