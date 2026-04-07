__all__ = ["EntityRandomSittingComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRandomSittingComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_sitting)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_sitting"

    cooldown: float = 0
    min_sit_time: float = 10
    start_chance: float = 0.1
    stop_chance: float = 0.3
