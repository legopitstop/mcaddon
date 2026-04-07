__all__ = ["EntityAreaAttackComponent"]

from mcaddon.library.constants import EntityDamageSource
from typing import ClassVar
from mcaddon.library.filter import Filter
from .component import EntityComponent


@EntityComponent.register
class EntityAreaAttackComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_area_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:area_attack"

    cause: EntityDamageSource
    damage_cooldown: float = 0
    damage_per_tick: int = 2
    damage_range: float = 0.2
    entity_filter: Filter
    play_attack_sound: bool = True
