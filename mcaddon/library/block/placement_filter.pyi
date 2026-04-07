from .component import BlockComponent, BlockFilter
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import BlockFace

__all__ = ["BlockPlacementFilterComponent"]

class PlacementCondition(BaseModel):
    allowed_faces: list[BlockFace]
    block_filter: list[BlockFilter | str]

class BlockPlacementFilterComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_placement_filter)
    """

    conditions: list[PlacementCondition]
