__all__ = ["EntityLookAtPlayerComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityLookAtPlayerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_player)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.look_at_player"
    angle_of_view_horizontal: int = 360
    angle_of_view_vertical: int = 360
    look_distance: float = 8
    look_time: Optional[NumberRange] = None
    max_look_time: Optional[float] = None
    min_look_time: Optional[float] = None
    probability: float = 0.02
    target_distance: Optional[float] = None
