__all__ = ["BlockRandomOffsetComponent", "RandomOffset"]

from typing import Optional, ClassVar
from mcaddon.core.base import BaseModel, NumberRange
from .component import BlockComponent


class RandomOffset(BaseModel):
    range: NumberRange
    steps: int


@BlockComponent.register
class BlockRandomOffsetComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_random_offset)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:random_offset"

    x: Optional[RandomOffset] = None
    y: Optional[RandomOffset] = None
    z: Optional[RandomOffset] = None
