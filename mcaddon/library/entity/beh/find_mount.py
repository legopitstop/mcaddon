__all__ = ["EntityFindMountComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityFindMountComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_mount)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.find_mount"

    avoid_water: bool = False
    max_failed_attempts: Optional[float] = None
    mount_distance: float = -1
    start_delay: int = 0
    target_needed: bool = False
    within_radius: float = 0
