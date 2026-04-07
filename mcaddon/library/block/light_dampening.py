__all__ = [
    "BlockLightDampeningComponent",
]


from mcaddon.core.base import ValueComponent
from pydantic import Field
from typing import ClassVar
from .component import BlockComponent


@BlockComponent.register
class BlockLightDampeningComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_light_dampening)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:light_dampening"

    value: int = Field(ge=0, le=15, default=15)
