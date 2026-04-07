__all__ = ["EntityAquaticChargeAttackComponent"]

from typing import ClassVar, List, Optional
from pydantic import Field

from mcaddon.core.base import NumberRange, NumberMinMax
from mcaddon.library.constants import ControlFlags
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityAquaticChargeAttackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_aquatic_charge_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.aquatic_charge_attack"

    max_charge_distance: int = 16
    charge_speed_multiplier: float = 0.05999999865889549
    charge_speed: Optional[float] = None
    attack_reach: float = 0.05000000074505806
    knockback_force: float = 2
    charge_overshoot_distance: float = 1.5
    charge_cooldown_time: NumberRange = NumberMinMax(min=2, max=6)
    control_flags: List[ControlFlags] = Field(default_factory=list)
