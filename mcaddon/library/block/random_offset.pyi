from .component import BlockComponent
from mcaddon.core.base import BaseModel, NumberRange

__all__ = ["BlockRandomOffsetComponent", "RandomOffset"]

class RandomOffset(BaseModel):
    range: NumberRange
    steps: int

class BlockRandomOffsetComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_random_offset)
    """

    x: RandomOffset | None
    y: RandomOffset | None
    z: RandomOffset | None
