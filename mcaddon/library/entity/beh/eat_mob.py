__all__ = ["EntityEatMobComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityEatMobComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_mob)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.eat_mob"

    eat_animation_time: float = 1
    eat_mob_sound: Optional[str] = None
    loot_table: Optional[str] = None
    pull_in_force: float = 1
    reach_mob_distance: float = 1
    run_speed: float = 1
