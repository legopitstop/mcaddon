__all__ = ["EntityTradeWithPlayerComponent"]

from typing import Optional, ClassVar
from mcaddon.library.filter import Filter
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityTradeWithPlayerComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_trade_with_player)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.trade_with_player"

    filters: Optional[Filter] = None
    max_distance_from_player: float = 0
