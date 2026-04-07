__all__ = [
    "BlockCustomComponentsComponent",
]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import ValueComponent
from ..component import BlockComponent
from deprecated import deprecated


@deprecated("This component is deprecated, register your own component instead.")
@BlockComponent.register
class BlockCustomComponentsComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_custom_components)

    This type is now deprecated, and no longer in use in the latest versions of Minecraft.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:custom_components"

    value: List[str] = Field(default_factory=list)
