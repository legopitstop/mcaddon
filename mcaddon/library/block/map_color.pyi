from .component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["BlockMapColorComponent"]

class BlockMapColorComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_map_color)
    """

    value: str
