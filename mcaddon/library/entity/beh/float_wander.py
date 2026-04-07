__all__ = ["EntityFloatWanderComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityFloatWanderComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float_wander)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.float_wander"

    additional_collision_buffer: bool = False
    allow_navigating_through_liquids: bool = False
    float_duration: Optional[NumberRange] = None
    float_wander_has_move_control: bool = True
    must_reach: bool = False
    navigate_around_surface: bool = False
    random_reselect: bool = False
    surface_xz_dist: int = 0
    surface_y_dist: int = 0
    use_home_position_restriction: bool = True
    xz_dist: int = 10
    y_dist: int = 7
    y_offset: int = 0
