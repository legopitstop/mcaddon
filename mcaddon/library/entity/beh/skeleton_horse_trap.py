__all__ = ["EntitySkeletonHorseTrapComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySkeletonHorseTrapComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_skeleton_horse_trap)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.skeleton_horse_trap"

    duration: float = 1
    within_radius: float = 0
