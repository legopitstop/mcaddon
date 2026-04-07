__all__ = ["EntitySonicBoomComponent"]

from typing import Optional, ClassVar
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntitySonicBoomComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sonic_boom)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.sonic_boom"

    attack_cooldown: float = 5
    attack_damage: float = 30
    attack_range_horizontal: float = 15
    attack_range_vertical: float = 20
    attack_sound: Optional[str] = None
    charge_sound: Optional[str] = None
    duration: float = 0
    duration_until_attack_sound: float = 1.7
    knockback_height_cap: float = 0
    knockback_horizontal_strength: float = 0
    knockback_vertical_strength: float = 0
    speed_multiplier: float = 1
