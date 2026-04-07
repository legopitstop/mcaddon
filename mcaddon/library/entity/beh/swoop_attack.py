__all__ = ["EntitySwoopAttackComponent"]

from typing import Optional, ClassVar
from mcaddon.core.base import NumberRange
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntitySwoopAttackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swoop_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.swoop_attack"

    damage_reach: float = 0.2
    delay_range: Optional[NumberRange] = None
    speed_multiplier: float = 1
