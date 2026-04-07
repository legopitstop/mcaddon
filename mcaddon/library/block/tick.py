__all__ = [
    "BlockTickComponent",
]

from typing import Tuple, ClassVar
from pydantic import Field

from .component import BlockComponent


@BlockComponent.register
class BlockTickComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_tick)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:tick"

    interval_range: Tuple[int, int] = Field(default=(0, 0))
    looping: bool = True
