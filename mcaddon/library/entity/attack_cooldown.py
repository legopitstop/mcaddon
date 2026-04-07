__all__ = ["EntityAttackCooldownComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntityAttackCooldownComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_attack_cooldown)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:attack_cooldown"

    # damage: int
    # effect_duration: int = 0
    # effect_name: str
    attack_cooldown_complete_event: Optional[EntityTriggerEvent] = None
    attack_cooldown_time: Optional[NumberRange | float] = None
