__all__ = [
    "BlockFrictionComponent",
]


from mcaddon.core.base import ValueComponent
from typing import ClassVar
from .component import BlockComponent


@BlockComponent.register
class BlockFrictionComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_friction)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:friction"

    value: float
