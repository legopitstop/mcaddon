from .component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["BlockLightDampeningComponent"]

class BlockLightDampeningComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_light_dampening)
    """

    value: int = ...
