from .component import BlockComponent
from mcaddon.core.base import BaseModel, ItemTags

__all__ = ["BlockDestructibleByMiningComponent"]

class ItemSpecificSpeeds(BaseModel):
    destroy_speed: float
    item: str | list[str] | ItemTags

class BlockDestructibleByMiningComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_mining)
    """

    seconds_to_destroy: float
    item_specific_speeds: list[ItemSpecificSpeeds]
