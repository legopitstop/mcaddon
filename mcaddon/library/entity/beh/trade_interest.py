__all__ = ["EntityTradeInterestComponent"]

from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent
from typing import ClassVar


@EntityComponent.register
class EntityTradeInterestComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_trade_interest)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.trade_interest"

    carried_item_switch_time: float = 2
    cooldown: float = 2
    interest_time: float = 45
    remove_item_time: float = 1
    within_radius: float = 0
