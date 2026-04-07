__all__ = ["EntityDamageSensorComponent", "DamageSensorTrigger"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import DealsDamage, EntityDamageSource
from .event import EntityTriggerEvent
from .component import EntityComponent


class DamageSensorTrigger(BaseModel):
    on_damage: Optional[EntityTriggerEvent] = None
    cause: EntityDamageSource = EntityDamageSource.NONE
    damage_modifier: int = 0
    damage_multiplier: float = 1
    deals_damage: bool | DealsDamage = False
    on_damage_sound_event: Optional[str] = None


@EntityComponent.register
class EntityDamageSensorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_damage_sensor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:damage_sensor"

    triggers: List[DamageSensorTrigger] | DamageSensorTrigger = Field(
        default_factory=list
    )
    deals_damage: Optional[DealsDamage | bool] = None
