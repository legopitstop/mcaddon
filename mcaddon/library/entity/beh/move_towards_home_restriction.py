__all__ = ["EntityMoveTowardsHomeRestrictionComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityMoveTowardsHomeRestrictionComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_home_restriction)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_towards_home_restriction"

    speed_multiplier: float = 1
