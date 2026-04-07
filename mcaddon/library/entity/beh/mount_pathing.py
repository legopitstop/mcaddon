__all__ = ["EntityMountPathingComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityMountPathingComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_mount_pathing)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.mount_pathing"

    speed_multiplier: float = 1
    target_dist: float = 0
    track_target: bool = False
