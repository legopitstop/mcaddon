__all__ = ["EntityJumpAroundTargetComponent"]

from typing import List, Optional, ClassVar
from mcaddon.library.filter import Filter
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityJumpAroundTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_jump_around_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.jump_around_target"

    check_collision: bool = False
    entity_bounding_box_scale: float = 0.7
    filters: Optional[Filter] = None
    jump_angles: List[float] = [40, 55, 60, 75, 80]
    jump_cooldown_duration: float = 0.5
    jump_cooldown_when_hurt_duration: float = 0.1
    landing_distance_from_target: Optional[NumberRange] = None
    landing_position_spread_degrees: int = 90
    last_hurt_duration: float = 2
    line_of_sight_obstruction_height_ignore: int = 4
    max_jump_velocity: float = 1.4
    prepare_jump_duration: float = 0.5
    required_vertical_space: int = 4
    snap_to_surface_block_range: int = 10
    valid_distance_to_target: Optional[NumberRange] = None
