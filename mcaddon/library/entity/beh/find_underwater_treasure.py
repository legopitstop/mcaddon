__all__ = ["EntityFindUnderwaterTreasureComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityFindUnderwaterTreasureComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_underwater_treasure)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.find_underwater_treasure"

    search_range: int = 0
    speed_multiplier: float = 1
    stop_distance: float = 2
