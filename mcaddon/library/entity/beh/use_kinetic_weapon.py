__all__ = ["EntityUseKineticWeaponComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
)


@EntityComponent.register
class EntityUseKineticWeaponComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_use_kinetic_weapon)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.use_kinetic_weapon"

    track_target: bool
    approach_distance: float
    weapon_reach_multiplier: float
    weapon_min_speed_multiplier: float
    hijack_mount_navigation: bool
    reposition_distance: NumberRange
    cooldown_distance: NumberRange
    cooldown_speed_multiplier: Optional[float] = None
    reposition_speed_multiplier: Optional[float] = None
    speed_multiplier: Optional[float] = None
