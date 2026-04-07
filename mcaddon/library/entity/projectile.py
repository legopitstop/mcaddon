__all__ = [
    "EntityProjectileComponent",
    "ProjectileHitEvent",
    "ProjectileImpactDamage",
    "ProjectileArrowEffect",
    "ProjectileStickInGround",
]

from typing import Optional, List, ClassVar
from pydantic import Field, BaseModel
from mcaddon.library.filter import Filter
from mcaddon.core.types import Vector3
from mcaddon.core.base import NumberRange
from .component import EntityComponent


class ProjectileImpactDamage(BaseModel):
    damage: NumberRange | float
    knockback: bool = True
    semi_random_diff_damage: bool = False
    destroy_on_hit: bool = True


class ProjectileStickInGround(BaseModel):
    shake_time: float = 0.35


class ProjectileArrowEffect(BaseModel):
    apply_effect_to_blocking_targets: bool = False


class ProjectileHitEvent(BaseModel):
    impact_damage: Optional[ProjectileImpactDamage] = None
    stick_in_ground: Optional[ProjectileStickInGround] = None
    arrow_effect: Optional[ProjectileStickInGround] = None


@EntityComponent.register
class EntityProjectileComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_projectile)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:projectile"

    angle_offset: float = 0
    catch_fire: bool = False
    crit_particle_on_hurt: bool = False
    destroy_on_hurt: bool = False
    filter: Optional[Filter] = None
    fire_affected_by_griefing: bool = False
    gravity: float = 0.05
    hit_nearest_passenger: bool = False
    hit_sound: Optional[str] = None
    homing: bool = False
    ignored_entities: List[str] = Field(default_factory=list)
    inertia: float = 0.99
    is_dangerous: bool = False
    knockback: bool = True
    lightning: bool = False
    liquid_inertia: float = 0.6
    multiple_targets: bool = True
    offset: Vector3 = (0, 0, 0)
    on_fire_time: float = 5
    particle: str = "iconcrack"
    potion_effect: int = -1
    power: float = 1.3
    reflect_immunity: float = 0
    reflect_on_hurt: bool = False
    semi_random_diff_damage: bool = False
    shoot_sound: Optional[str] = None
    shoot_target: bool = True
    should_bounce: bool = False
    splash_potion: bool = False
    splash_range: float = 4
    uncertainty_base: float = 0
    uncertainty_multiplier: float = 0
    on_hit: Optional[ProjectileHitEvent] = None
    anchor: Optional[int] = None
    destroyOnHurt: Optional[bool] = None
    hit_ground_sound: Optional[str] = None
    stop_on_hurt: Optional[bool] = None
    isolated_physics: Optional[bool] = None
