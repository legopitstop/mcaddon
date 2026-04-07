from .component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["BlockLightEmissionComponent"]

class BlockLightEmissionComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_light_emission)
    """

    value: int = ...
