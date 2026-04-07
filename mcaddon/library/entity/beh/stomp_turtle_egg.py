__all__ = ["EntityStompTurtleEggComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityStompTurtleEggComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stomp_turtle_egg)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.stomp_turtle_egg"

    goal_radius: float = 0.5
    interval: int = 120
    search_height: int = 1
    search_range: int = 0
    speed_multiplier: int = 1
