__all__ = [
    "BlockDestructibleByMiningComponent",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, ItemTags
from .component import BlockComponent


class ItemSpecificSpeeds(BaseModel):
    destroy_speed: float
    item: str | List[str] | ItemTags = Field(default_factory=list)


@BlockComponent.register
class BlockDestructibleByMiningComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_mining)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:destructible_by_mining"

    seconds_to_destroy: float = 0.0
    item_specific_speeds: List[ItemSpecificSpeeds] = Field(default_factory=list)
