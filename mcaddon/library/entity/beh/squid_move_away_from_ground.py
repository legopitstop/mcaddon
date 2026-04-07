__all__ = ["EntitySquidMoveAwayFromGroundComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntitySquidMoveAwayFromGroundComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_move_away_from_ground)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.squid_move_away_from_ground"
