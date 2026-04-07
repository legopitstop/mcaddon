from .component import BlockComponent
from mcaddon.library.constants import SupportShape as SupportShape

__all__ = ["BlockSupportComponent", "SupportShape"]

class BlockSupportComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_support)
    """

    shape: SupportShape
