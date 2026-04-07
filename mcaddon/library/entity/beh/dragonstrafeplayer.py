__all__ = ["EntityDragonStrafePlayerComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityDragonStrafePlayerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dragonstrafeplayer)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.dragonstrafeplayer"

    active_speed: float = 0.6
    fireball_range: float = 64
    flight_speed: float = 0.6
    switch_direction_probability: float = 0.125
    target_in_range_and_in_view_time: float = 0.25
    target_zone: Optional[NumberRange] = None
    turn_speed: float = 0.7
    view_angle: float = 10
