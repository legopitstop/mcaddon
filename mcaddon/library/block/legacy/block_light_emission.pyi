from ..component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["LegacyBlockLightEmissionComponent"]

class LegacyBlockLightEmissionComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_block_light_emission)

    Use minecraft:light_emission in newer format versions.
    """

    value: int = ...
