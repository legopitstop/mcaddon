__all__ = ["EntityChargeAttackComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityChargeAttackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_charge_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.charge_attack"

    max_distance: int = 3
    min_distance: int = 2
    speed_multiplier: float = 1
    success_rate: float = 0.1428
