__all__ = ["EntityRandomLookAroundComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityRandomLookAroundComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_look_around)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_look_around"

    look_distance: Optional[float] = None
    look_time: Optional[NumberRange] = None
    max_angle_of_view_horizontal: int = 30
    min_angle_of_view_horizontal: int = -30
