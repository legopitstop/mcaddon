__all__ = [
    "LegacyBlockLightEmissionComponent",
]


from mcaddon.core.base import ValueComponent
from pydantic import Field
from typing import ClassVar
from ..component import BlockComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use BlockLightEmissionComponent instead.")
@BlockComponent.register
class LegacyBlockLightEmissionComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_block_light_emission)

    Use minecraft:light_emission in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:block_light_emission"
    format_version = "<1.19.40"

    value: int = Field(ge=0, le=15, default=15)
