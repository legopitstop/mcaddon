__all__ = ["EntityRandomFlyComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityRandomFlyComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_fly)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.random_fly"

    avoid_damage_blocks: Optional[bool] = None
    can_land_on_trees: bool = True
    speed_multiplier: float = 1
    xz_dist: int = 10
    y_dist: int = 7
    y_offset: Optional[float] = 0
