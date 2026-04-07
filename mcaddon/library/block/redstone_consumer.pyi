from .component import BlockComponent

__all__ = ["BlockRedstoneConsumerComponent"]

class BlockRedstoneConsumerComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_consumer)
    """

    min_power: int = ...
    propagates_power: bool = ...
