__all__ = ["EntitySlimeRandomDirectionComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySlimeRandomDirectionComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_random_direction)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.slime_random_direction"

    add_random_time_range: int = 3
    min_change_direction_time: float = 2
    turn_range: int = 360
