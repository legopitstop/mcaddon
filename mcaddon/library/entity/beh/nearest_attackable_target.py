__all__ = ["EntityNearestAttackableTargetComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field, BaseModel
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


class NearestAttackableEntity(BaseModel):
    pass


@EntityComponent.register
class EntityNearestAttackableTargetComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nearest_attackable_target)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.nearest_attackable_target"

    attack_interval: Optional[NumberRange | int] = None
    attack_interval_min: Optional[float] = None
    attack_owner: bool = False
    entity_types: List[NearestAttackableEntity] | NearestAttackableEntity = Field(
        default_factory=list
    )
    must_reach: bool = False
    must_see: bool = False
    must_see_forget_duration: float = 3
    persist_time: float = 0
    reselect_targets: bool = False
    scan_interval: int = 10
    set_persistent: bool = False
    target_acquisition_probability: float = 1
    target_invisible_multiplier: float = 0.7
    target_search_height: float = -1
    target_sneak_visibility_multiplier: float = 0.8
    within_radius: float = 0
