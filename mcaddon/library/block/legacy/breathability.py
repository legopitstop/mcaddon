__all__ = [
    "BlockBreathabilityComponent",
]

from ..component import BlockComponent
from typing import ClassVar
from deprecated import deprecated


@deprecated("This component is deprecated.")
@BlockComponent.register
class BlockBreathabilityComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_breathability)

    This type is now deprecated, and no longer in use in the latest versions of Minecraft.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:breathability"
