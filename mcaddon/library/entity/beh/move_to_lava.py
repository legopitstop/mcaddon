__all__ = ["EntityMoveToLavaComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityMoveToLavaComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_lava)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_to_lava"

    goal_radius: float = 0.5
    search_count: int = 10
    search_height: int = 1
    search_range: int = 0
    speed_multiplier: float = 1
