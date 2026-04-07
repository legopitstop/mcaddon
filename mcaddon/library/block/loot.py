__all__ = [
    "BlockLootComponent",
]


from mcaddon.core.base import ValueComponent
from typing import ClassVar
from .component import BlockComponent


@BlockComponent.register
class BlockLootComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_loot)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:loot"

    value: str
