from .component import BlockComponent
from mcaddon.core.base import ValueComponent
from mcaddon.core.types import Vector3

__all__ = ["BlockCollisionBoxComponent"]

class BlockCollisionBoxComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_collision_box)
    """

    origin: Vector3 = ...
    size: Vector3 = ...
