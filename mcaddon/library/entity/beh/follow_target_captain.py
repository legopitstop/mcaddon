__all__ = ["EntityFollowTargetCaptainComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityFollowTargetCaptainComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_target_captain)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.follow_target_captain"

    follow_distance: float = 0
    speed_multiplier: Optional[float] = None
    within_radius: float = 0
