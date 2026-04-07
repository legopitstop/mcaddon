__all__ = ["EntityFloatComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityFloatComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.float"

    chance_per_tick_to_float: float = 0.8
    sink_with_passengers: Optional[int] = None
    time_under_water_to_dismount_passengers: Optional[float] = None
