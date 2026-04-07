__all__ = ["EntityPanicComponent", "SoundInterval"]

from typing import Optional, List, ClassVar
from pydantic import Field, BaseModel
from mcaddon.library.constants import EntityDamageSource
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


class SoundInterval(BaseModel):
    range_max: Optional[float] = None
    range_min: Optional[float] = None


@EntityComponent.register
class EntityPanicComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_panic)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.panic"

    damage_sources: List[EntityDamageSource] = Field(default_factory=list)
    force: bool = False
    ignore_mob_damage: bool = False
    panic_sound: Optional[str] = None
    prefer_water: bool = False
    sound_interval: Optional[SoundInterval] = None
    speed_multiplier: float = 0
