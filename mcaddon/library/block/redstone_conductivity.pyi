from .component import BlockComponent

__all__ = ["BlockRedstoneConductivityComponent"]

class BlockRedstoneConductivityComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_conductivity)
    """

    allows_wire_to_step_down: bool
    redstone_conductor: bool
