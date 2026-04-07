__all__ = ["BlockSupportComponent", "SupportShape"]


from mcaddon.library.constants import SupportShape
from typing import ClassVar
from .component import BlockComponent


@BlockComponent.register
class BlockSupportComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_support)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:support"

    shape: SupportShape
