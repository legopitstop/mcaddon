__all__ = [
    "LegacyBlockLightAbsorptionComponent",
]


from typing import ClassVar
from pydantic import Field

from mcaddon.core.base import ValueComponent
from ..component import BlockComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use BlockLightDampeningComponent instead.")
@BlockComponent.register
class LegacyBlockLightAbsorptionComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_block_light_absorption)

    Use minecraft:light_dampening in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:block_light_absorption"
    format_version = "<1.19.40"

    value: int = Field(ge=0, le=15, default=15)
