__all__ = ["EntityInsideBlockNotifierComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, BlockLike
from .event import EntityTriggerEvent
from .component import EntityComponent


class InsideBlockList(BaseModel):
    block: BlockLike
    entered_block_event: Optional[EntityTriggerEvent] = None
    exited_block_event: Optional[EntityTriggerEvent] = None


@EntityComponent.register
class EntityInsideBlockNotifierComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_inside_block_notifier)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:inside_block_notifier"

    block_list: List[InsideBlockList] = Field(default_factory=list)
