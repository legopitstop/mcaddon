__all__ = [
    "BlockDestructibleByExplosionComponent",
]

from .component import BlockComponent
from typing import ClassVar


@BlockComponent.register
class BlockDestructibleByExplosionComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_explosion)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:destructible_by_explosion"

    explosion_resistance: float = 0.0
