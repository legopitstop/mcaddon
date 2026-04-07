__all__ = [
    "BlockMapColorComponent",
]


from mcaddon.core.base import ValueComponent
from typing import ClassVar
from .component import BlockComponent


@BlockComponent.register
class BlockMapColorComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_map_color)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:map_color"

    value: str
