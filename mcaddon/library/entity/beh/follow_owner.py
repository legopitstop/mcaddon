__all__ = ["EntityFollowOwnerComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityFollowOwnerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_owner)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.follow_owner"

    speed_multiplier: int = 0
    start_distance: int = 0
    stop_distance: int = 0
    can_teleport: bool = False
    ignore_vibration: bool = False
