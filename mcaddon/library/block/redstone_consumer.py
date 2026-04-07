__all__ = [
    "BlockRedstoneConsumerComponent",
]


from .component import BlockComponent
from typing import ClassVar


@BlockComponent.register
class BlockRedstoneConsumerComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_consumer)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:redstone_consumer"

    min_power: int = 0
    propagates_power: bool = False
