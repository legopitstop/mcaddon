__all__ = ["EntityMeleeBoxAttackComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityMeleeBoxAttackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_melee_box_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.melee_box_attack"

    attack_once: bool = False
    attack_types: Optional[str] = None
    can_spread_on_fire: bool = False
    cooldown_time: float = 1
    horizontal_reach: float = 0.8
    inner_boundary_time_increase: float = 0.25
    max_path_time: float = 0.55
    melee_fov: float = 90
    min_path_time: float = 0.2
    on_attack: Optional[EntityTriggerEvent] = None
    on_kill: Optional[EntityTriggerEvent] = None
    outer_boundary_time_increase: float = 0.5
    path_fail_time_increase: float = 0.75
    path_inner_boundary: float = 16
    path_outer_boundary: float = 32
    random_stop_interval: int = 0
    require_complete_path: bool = False
    speed_multiplier: float = 1
    track_target: bool = False
    x_max_rotation: float = 30
    y_max_head_rotation: float = 30
