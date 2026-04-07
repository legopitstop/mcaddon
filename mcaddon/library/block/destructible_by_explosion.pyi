from .component import BlockComponent

__all__ = ["BlockDestructibleByExplosionComponent"]

class BlockDestructibleByExplosionComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_explosion)
    """

    explosion_resistance: float
