from ..component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["LegacyBlockLightAbsorptionComponent"]

class LegacyBlockLightAbsorptionComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_block_light_absorption)

    Use minecraft:light_dampening in newer format versions.
    """

    value: int = ...
