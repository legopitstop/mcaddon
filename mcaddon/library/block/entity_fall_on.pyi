from .component import BlockComponent

__all__ = ["BlockEntityFallOnComponent"]

class BlockEntityFallOnComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_entity_fall_on)
    """

    min_fall_distance: float
