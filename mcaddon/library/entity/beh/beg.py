__all__ = ["EntityBegComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityBegComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_beg)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.beg"

    items: List[str] = Field(default_factory=list)
    look_distance: float = 8
    look_time: Optional[NumberRange] = None
