from .component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["BlockDisplayNameComponent"]

class BlockDisplayNameComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_display_name)
    """

    value: str
