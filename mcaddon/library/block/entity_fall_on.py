__all__ = [
    "BlockEntityFallOnComponent",
]


from .component import BlockComponent
from typing import ClassVar


@BlockComponent.register
class BlockEntityFallOnComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_entity_fall_on)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:entity_fall_on"

    min_fall_distance: float
