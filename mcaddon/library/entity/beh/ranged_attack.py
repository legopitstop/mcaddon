__all__ = ["EntityRangedAttackComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityRangedAttackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ranged_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.ranged_attack"

    attack_interval: float = 0
    attack_interval_max: float = 0
    attack_interval_min: float = 0
    attack_radius: float = 0
    attack_radius_min: float = 0
    burst_interval: float = 0
    burst_shots: int = 1
    charge_charged_trigger: float = 0
    charge_shoot_trigger: float = 0
    ranged_fov: float = 90
    set_persistent: bool = False
    speed_multiplier: float = 1
    swing: bool = False
    target_in_sight_time: float = 1
    x_max_rotation: float = 30
    y_max_head_rotation: float = 30
