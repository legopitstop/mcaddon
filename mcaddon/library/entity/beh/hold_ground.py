__all__ = ["EntityHoldGroundComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityHoldGroundComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hold_ground)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.hold_ground"

    broadcast: bool = False
    broadcast_range: float = 0
    min_radius: float = 10
    within_radius_event: Optional[EntityTriggerEvent] = None
