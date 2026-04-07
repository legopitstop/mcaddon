from .component import BlockComponent
from mcaddon.library.constants import Direction

__all__ = ["BlockRedstoneProducerComponent"]

class BlockRedstoneProducerComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_producer)
    """

    connected_faces: list[Direction]
    power: int
    strongly_powered_face: Direction | None
    transform_relative: bool
