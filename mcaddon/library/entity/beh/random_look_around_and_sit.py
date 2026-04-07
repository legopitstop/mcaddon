__all__ = ["EntityRandomLookAroundAndSitComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRandomLookAroundAndSitComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_look_around_and_sit)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_look_around_and_sit"

    continue_if_leashed: bool = False
    continue_sitting_on_reload: bool = False
    max_angle_of_view_horizontal: float = 30
    max_look_count: int = 2
    max_look_time: int = 40
    min_angle_of_view_horizontal: float = -30
    min_look_count: int = 1
    min_look_time: int = 20
    probability: float = 0.02
    random_look_around_cooldown: int = 0
