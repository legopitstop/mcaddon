__all__ = ["EntityTransportItemsComponent"]

from typing import List, Tuple, ClassVar, Optional
from pydantic import Field
from mcaddon.core.base import BlockLike
from mcaddon.library.constants import TransportSearchStrategy, TransportPlaceStrategy
from mcaddon.library.entity.component import (
    EntityComponent,
    EntityBehaviorComponent,
)


@EntityComponent.register
class EntityTransportItemsComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_transport_items)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.transport_items"

    source_container_types: List[BlockLike] = Field(default_factory=list)
    destination_container_types: List[BlockLike] = Field(default_factory=list)
    max_stack_size: int
    interaction_time: Optional[float] = None
    allow_simultaneous_interaction: Optional[bool] = None
    search_strategy: TransportSearchStrategy
    search_distance: Tuple[int, int]
    max_visited_containers: int
    initial_cooldown: int
    idle_cooldown: int
    place_strategy: TransportPlaceStrategy
