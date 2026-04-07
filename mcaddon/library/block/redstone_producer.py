__all__ = [
    "BlockRedstoneProducerComponent",
]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.library.constants import Direction
from .component import BlockComponent


@BlockComponent.register
class BlockRedstoneProducerComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_producer)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:redstone_producer"

    connected_faces: List[Direction] = Field(default_factory=list)
    power: int
    strongly_powered_face: Optional[Direction]
    transform_relative: bool = False
