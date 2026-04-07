__all__ = [
    "BlockRedstoneConductivityComponent",
]


from .component import BlockComponent
from typing import ClassVar


@BlockComponent.register
class BlockRedstoneConductivityComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_conductivity)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:redstone_conductivity"

    allows_wire_to_step_down: bool = True
    redstone_conductor: bool = False
