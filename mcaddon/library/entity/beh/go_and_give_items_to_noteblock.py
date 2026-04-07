__all__ = ["EntityGoAndGiveItemsToNoteblockComponent"]

from typing import List, Optional, ClassVar

from pydantic import Field
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from mcaddon.library.entity.event import EntityTriggerEvent


@EntityComponent.register
class EntityGoAndGiveItemsToNoteblockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_go_and_give_items_to_noteblock)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.go_and_give_items_to_noteblock"

    run_speed: int = 0
    throw_sound: Optional[str] = None
    on_item_throw: List[EntityTriggerEvent] = Field(default_factory=list)
