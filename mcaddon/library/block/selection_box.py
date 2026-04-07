__all__ = [
    "BlockSelectionBoxComponent",
]

from mcaddon.core.base import ValueComponent
from typing import ClassVar
from mcaddon.core.types import Vector3
from .component import BlockComponent


@BlockComponent.register
class BlockSelectionBoxComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_selection_box)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:selection_box"

    origin: Vector3 = (-8, 0, -8)
    size: Vector3 = (16, 16, 16)

    @classmethod
    def _wrap_parse(cls, v, handler):
        if isinstance(v, bool):
            if v:
                v = {"origin": [-8, 0, -8], "size": [16, 16, 16]}
            else:
                v = {"origin": [-8, 0, -8], "size": [0, 0, 0]}
        return handler(v)
