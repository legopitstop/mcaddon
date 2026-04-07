__all__ = ["EntityPlayDeadComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.library.constants import EntityDamageSource
from mcaddon.core.base import NumberRange
from mcaddon.library.filter import Filter
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityPlayDeadComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_play_dead)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.play_dead"

    apply_regeneration: bool = False
    damage_sources: List[EntityDamageSource] = Field(default_factory=list)
    duration: float = 1
    filters: List[Filter] | Filter = Field(default_factory=list)
    force_below_health: int = 0
    random_damage_range: Optional[NumberRange] = None
    random_start_chance: float = 1
