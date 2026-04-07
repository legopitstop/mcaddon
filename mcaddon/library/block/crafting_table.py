__all__ = [
    "BlockCraftingTableComponent",
]

from typing import List, ClassVar
from pydantic import Field
from .component import BlockComponent


@BlockComponent.register
class BlockCraftingTableComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_crafting_table)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:crafting_table"

    crafting_tags: List[str] = Field(default_factory=list)
    table_name: str
