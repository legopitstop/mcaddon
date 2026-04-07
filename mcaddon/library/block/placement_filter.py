__all__ = [
    "BlockPlacementFilterComponent",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import BlockFace
from .component import BlockComponent, BlockFilter


class PlacementCondition(BaseModel):
    allowed_faces: List[BlockFace] = Field(default_factory=list)
    block_filter: List[BlockFilter | str] = Field(default_factory=list)


@BlockComponent.register
class BlockPlacementFilterComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_placement_filter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:placement_filter"

    conditions: List[PlacementCondition] = Field(default_factory=list)
