__all__ = ["EntitySlimeAttackComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySlimeAttackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_attack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.slime_attack"

    set_persistent: bool = False
    speed_multiplier: float = 1
    x_max_rotation: float = 10
    y_max_rotation: float = 10
