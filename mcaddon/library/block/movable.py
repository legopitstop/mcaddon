__all__ = [
    "BlockMovableComponent",
]

from typing import Optional, ClassVar
from mcaddon.library.constants import MovementType, MoveableSticky
from .component import BlockComponent


@BlockComponent.register
class BlockMovableComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_movable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:movable"

    movement_type: MovementType = MovementType.PUSH_PULL
    sticky: Optional[MoveableSticky] = MoveableSticky.NONE
