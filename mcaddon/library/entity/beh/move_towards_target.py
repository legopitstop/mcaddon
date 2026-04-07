__all__ = ["EntityMoveTowardsTargetComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityMoveTowardsTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_towards_target"

    speed_multiplier: Optional[float] = None
    within_radius: float = 0
