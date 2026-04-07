__all__ = ["EntityPlaceBlockComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.library.filter import Filter
from mcaddon.core.base import NumberRange, BlockLike, BaseModel
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


class RandomlyPlaceableBlock(BaseModel):
    block: BlockLike
    filter: Filter


@EntityComponent.register
class EntityPlaceBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_place_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.place_block"

    affected_by_griefing_rule: Optional[bool] = None
    can_place: Optional[Filter] = None
    chance: Optional[float] = None
    on_place: Optional[EntityTriggerEvent] = None
    placeable_carried_blocks: List[str] = Field(default_factory=list)
    randomly_placeable_blocks: List[str | RandomlyPlaceableBlock] = Field(
        default_factory=list
    )
    xz_range: Optional[NumberRange | int] = None
    y_range: Optional[NumberRange | int] = None
