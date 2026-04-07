__all__ = ["EntityRandomHoverComponent"]

from typing import List, ClassVar
from pydantic import Field

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityRandomHoverComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_hover)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_hover"

    xz_dist: int = 0
    y_dist: int = 0
    y_offset: int = 0
    interval: int = 0
    hover_height: List[int] = Field(default_factory=list)
