from ..component import BlockComponent
from mcaddon.core.base import ValueComponent

__all__ = ["BlockCustomComponentsComponent"]

class BlockCustomComponentsComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_custom_components)

    This type is now deprecated, and no longer in use in the latest versions of Minecraft.
    """

    value: list[str]
