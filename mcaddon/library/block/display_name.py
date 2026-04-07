__all__ = [
    "BlockDisplayNameComponent",
]

from mcaddon.core.base import ValueComponent
from typing import ClassVar
from .component import BlockComponent


@BlockComponent.register
class BlockDisplayNameComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_display_name)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:display_name"

    value: str
