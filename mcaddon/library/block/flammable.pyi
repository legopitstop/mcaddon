from .component import BlockComponent

__all__ = ["BlockFlammableComponent"]

class BlockFlammableComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_flammable)
    """

    catch_chance_modifier: int
    destroy_chance_modifier: int
