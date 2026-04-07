from .component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["BlockLootComponent"]

class BlockLootComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_loot)
    """

    value: str
