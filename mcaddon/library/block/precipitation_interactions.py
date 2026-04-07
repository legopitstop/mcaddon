__all__ = ["BlockPrecipitationInteractionsComponent"]

from mcaddon.library.constants import PrecipitationBehavior
from typing import ClassVar
from .component import BlockComponent


@BlockComponent.register
class BlockPrecipitationInteractionsComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_precipitation_interactions)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:precipitation_interactions"

    precipitation_behavior: PrecipitationBehavior
