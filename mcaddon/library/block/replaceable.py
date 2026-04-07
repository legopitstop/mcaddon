__all__ = [
    "BlockReplaceableComponent",
]

from .component import BlockComponent
from typing import ClassVar


@BlockComponent.register
class BlockReplaceableComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_replaceable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:replaceable"
