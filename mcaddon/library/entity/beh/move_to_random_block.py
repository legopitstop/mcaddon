__all__ = ["EntityMoveToRandomBlockComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityMoveToRandomBlockComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_random_block)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_to_random_block"

    block_distance: float = 16
    speed_multiplier: Optional[float] = None
    within_radius: float = 0
