from .component import BlockComponent
from mcaddon.library.constants import MoveableSticky, MovementType

__all__ = ["BlockMovableComponent"]

class BlockMovableComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_movable)
    """

    movement_type: MovementType
    sticky: MoveableSticky | None
