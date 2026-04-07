__all__ = ["EntityKnockbackRoarComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import Filter
from mcaddon.library.entity.event import EntityTriggerEvent
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityKnockbackRoarComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_knockback_roar)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.knockback_roar"

    attack_time: float = 0.5
    cooldown_time: float = 0.1
    damage_filters: Optional[Filter] = None
    duration: float = 1
    knockback_damage: int = 6
    knockback_filters: Optional[Filter] = None
    knockback_height_cap: float = 0.4
    knockback_horizontal_strength: int = 4
    knockback_range: int = 4
    knockback_vertical_strength: int = 4
    on_roar_end: Optional[EntityTriggerEvent] = None
