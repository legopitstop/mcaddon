__all__ = ["EntityBehaviorAdmireItemComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityBehaviorAdmireItemComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_admire_item)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.admire_item"

    admire_item_sound: Optional[str] = None
    on_admire_item_start: Optional[EntityTriggerEvent] = None
    on_admire_item_stop: Optional[EntityTriggerEvent] = None
    sound_interval: NumberRange | int = 0
