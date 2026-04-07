__all__ = ["EntityMoveOutdoorsComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityMoveOutdoorsComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_outdoors)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_outdoors"

    goal_radius: float = 0.5
    search_count: int = 10
    search_height: int = 5
    search_range: int = 15
    speed_multiplier: float = 0.5
    timeout_cooldown: float = 8
