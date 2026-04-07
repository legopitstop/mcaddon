__all__ = ["EntityPreferredPathComponent"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class BlockPath(BaseModel):
    cost: int
    blocks: List[str] = Field(default_factory=list)


@EntityComponent.register
class EntityPreferredPathComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_preferred_path)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:preferred_path"

    default_block_cost: float = 0
    jump_cost: int = 0
    max_fall_blocks: int = 3
    preferred_path_blocks: List[BlockPath] = Field(default_factory=list)
