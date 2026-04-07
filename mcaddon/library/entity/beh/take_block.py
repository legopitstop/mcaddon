__all__ = ["EntityTakeBlockComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.library.filter import Filter
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityTakeBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_take_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.take_block"

    affected_by_griefing_rule: Optional[bool] = None
    blocks: List[str] = Field(default_factory=list)
    can_take: Optional[Filter] = None
    chance: Optional[float] = None
    on_take: Optional[EntityTriggerEvent] = None
    requires_line_of_sight: Optional[bool] = None
    xz_range: Optional[NumberRange] = None
    y_range: Optional[NumberRange] = None
