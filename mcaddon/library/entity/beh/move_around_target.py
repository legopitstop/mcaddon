__all__ = ["EntityMoveAroundTargetComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.filter import Filter
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityMoveAroundTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_around_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_around_target"

    destination_pos_spread_degrees: float = 90
    destination_position_range: Optional[NumberRange] = None
    filters: Optional[Filter] = None
    height_difference_limit: float = 10
    horizontal_search_distance: int = 5
    movement_speed: float = 0.6
    vertical_search_distance: int = 5
