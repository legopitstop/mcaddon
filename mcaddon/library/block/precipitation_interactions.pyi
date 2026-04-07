from .component import BlockComponent
from mcaddon.library.constants import PrecipitationBehavior

__all__ = ["BlockPrecipitationInteractionsComponent"]

class BlockPrecipitationInteractionsComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_precipitation_interactions)
    """

    precipitation_behavior: PrecipitationBehavior
