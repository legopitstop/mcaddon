__all__ = ["EntityPickupItemsComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import ItemTags
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


@EntityComponent.register
class EntityPickupItemsComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_pickup_items)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.pickup_items"

    can_pickup_any_item: bool = False
    can_pickup_to_hand_or_equipment: bool = True
    cooldown_after_being_attacked: Optional[float] = None
    excluded_items: List[str | ItemTags] = Field(default_factory=list)
    goal_radius: float = 0.5
    max_dist: float = 0
    pickup_based_on_chance: bool = False
    pickup_same_items_as_in_hand: Optional[bool] = None
    search_height: Optional[float] = None
    speed_multiplier: float = 1
    track_target: bool = False
