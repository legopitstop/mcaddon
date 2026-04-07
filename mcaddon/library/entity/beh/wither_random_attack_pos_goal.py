__all__ = ["EntityWitherRandomAttackPosGoalComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityWitherRandomAttackPosGoalComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_wither_random_attack_pos_goal)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.wither_random_attack_pos_goal"
