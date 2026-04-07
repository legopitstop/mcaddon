from .component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["BlockFrictionComponent"]

class BlockFrictionComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_friction)
    """

    value: float
