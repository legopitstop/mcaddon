from .component import BlockComponent

__all__ = ["BlockCraftingTableComponent"]

class BlockCraftingTableComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_crafting_table)
    """

    crafting_tags: list[str]
    table_name: str
