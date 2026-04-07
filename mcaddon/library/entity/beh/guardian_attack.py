__all__ = ["EntityGuardianAttackComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityGuardianAttackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_guardian_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.guardian_attack"

    elder_extra_magic_damage: int = 2
    hard_mode_extra_magic_damage: int = 2
    magic_damage: int = 1
    min_distance: float = 3
    sound_delay_time: float = 0.5
    x_max_rotation: float = 90
    y_max_head_rotation: float = 90
