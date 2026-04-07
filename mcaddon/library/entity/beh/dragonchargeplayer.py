__all__ = ["EntityDragonChargePlayerComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityDragonChargePlayerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dragonchargeplayer)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.dragonchargeplayer"

    active_speed: float = 3
    continue_charge_threshold_time: float = 0.5
    flight_speed: float = 0.6
    target_zone: Optional[NumberRange] = None
    turn_speed: float = 0.7
