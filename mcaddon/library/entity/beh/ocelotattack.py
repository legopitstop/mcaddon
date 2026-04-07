__all__ = ["EntityOcelotattackComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityOcelotattackComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ocelotattack)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.ocelotattack"

    cooldown_time: float = 1
    max_distance: float = 15
    max_sneak_range: float = 15
    max_sprint_range: float = 4
    reach_multiplier: float = 2
    sneak_speed_multiplier: float = 0.6
    sprint_speed_multiplier: float = 1.33
    walk_speed_multiplier: float = 0.8
    x_max_rotation: float = 30
    y_max_head_rotation: float = 30
