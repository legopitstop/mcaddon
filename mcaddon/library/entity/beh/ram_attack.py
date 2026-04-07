__all__ = ["EntityRamAttackComponent"]

from typing import Optional, List, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityRamAttackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ram_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.ram_attack"

    baby_knockback_modifier: float = 0.333333
    cooldown_range: Optional[NumberRange] = None
    knockback_force: float = 5
    knockback_height: float = 0.1
    min_ram_distance: int = 4
    on_start: Optional[EntityTriggerEvent | List[EntityTriggerEvent]] = None
    pre_ram_sound: Optional[str] = None
    ram_distance: int = 7
    ram_impact_sound: Optional[str] = None
    ram_speed: float = 2
    run_speed: float = 1
