__all__ = ["EntityFireAtTargetComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.filter import Filter
from mcaddon.core.types import Vector3
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityFireAtTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_fire_at_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.fire_at_target"

    attack_cooldown: float = 0.5
    attack_range: Optional[NumberRange] = None
    filters: Optional[Filter] = None
    max_head_rotation_x: float = 30
    max_head_rotation_y: float = 30
    owner_anchor: int = 2
    owner_offset: Vector3 = (0, 0, 0)
    post_shoot_delay: float = 0.2
    pre_shoot_delay: float = 0.75
    projectile_def: Optional[str] = None
    ranged_fov: float = 90
    target_anchor: int = 2
    target_offset: Vector3 = (0, 0, 0)
