__all__ = ["EntityJumpToBlockComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityJumpToBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_jump_to_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.jump_to_block"

    cooldown_range: Optional[NumberRange] = None
    forbidden_blocks: List[str] = Field(default_factory=list)
    max_velocity: float = 1.5
    minimum_distance: int = 2
    minimum_path_length: int = 5
    preferred_blocks: List[str] = Field(default_factory=list)
    preferred_blocks_chance: float = 1
    scale_factor: float = 0.7
    search_height: int = 10
    search_width: int = 8
