__all__ = ["EntityHurtOnConditionComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field, BaseModel

from mcaddon.library.filter import Filter
from mcaddon.library.constants import EntityDamageSource
from .component import EntityComponent


class DamageCondition(BaseModel):
    filters: Optional[Filter] = None
    cause: Optional[EntityDamageSource] = None
    damage_per_tick: int = 0


@EntityComponent.register
class EntityHurtOnConditionComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_hurt_on_condition)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:hurt_on_condition"

    damage_conditions: List[DamageCondition] = Field(default_factory=list)
