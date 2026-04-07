__all__ = [
    "BlockFlowerPottableComponent",
]


from .component import BlockComponent
from typing import ClassVar


@BlockComponent.register
class BlockFlowerPottableComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_flower_pottable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:flower_pottable"
