__all__ = ["EntityBreakBlocksComponent"]

from typing import List, ClassVar

from pydantic import Field
from .component import EntityComponent


@EntityComponent.register
class EntityBreakBlocksComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_break_blocks)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:break_blocks"

    breakable_blocks: List[str] = Field(default_factory=list)
