from .component import BlockComponent

__all__ = ["BlockTickComponent"]

class BlockTickComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_tick)
    """

    interval_range: tuple[int, int] = ...
    looping: bool = ...
