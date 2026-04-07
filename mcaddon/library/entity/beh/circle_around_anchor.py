__all__ = ["EntityCircleAroundAnchorComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
)
from mcaddon.core.base import NumberRange


@EntityComponent.register
class EntityCircleAroundAnchorComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_circle_around_anchor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.circle_around_anchor"

    angle_change: float = 15
    goal_radius: float = 0.5
    height_above_target_range: Optional[NumberRange] = None
    height_adjustment_chance: float = 0.002857
    height_offset_range: Optional[NumberRange] = None
    radius_adjustment_chance: float = 0.004
    radius_change: float = 1
    radius_range: Optional[NumberRange] = None
    speed_multiplier: int = 1
