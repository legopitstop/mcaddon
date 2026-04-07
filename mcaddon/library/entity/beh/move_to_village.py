__all__ = ["EntityMoveToVillageComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityMoveToVillageComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_village)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_to_village"

    cooldown_time: float = 0
    goal_radius: float = 0.5
    search_range: int = 0
    speed_multiplier: float = 1
