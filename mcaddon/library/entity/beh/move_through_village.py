__all__ = ["EntityMoveThroughVillageComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityMoveThroughVillageComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_through_village)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.move_through_village"

    only_at_night: bool = False
    speed_multiplier: float = 1
