__all__ = ["EntityAgeableComponent", "FeedItem"]

from typing import List, Optional, ClassVar
from pydantic import Field

from mcaddon.library.filter import FilterTest
from mcaddon.core.base import ItemResult
from .component import EntityComponent
from .event import EntityTriggerEvent


class FeedItem(ItemResult):
    growth: Optional[float] = None


@EntityComponent.register
class EntityAgeableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ageable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:ageable"

    drop_items: List[str] = Field(default_factory=list)
    duration: int = 1200
    grow_up: Optional[EntityTriggerEvent] = None
    interact_filters: Optional[FilterTest] = None
    feed_items: List[str | FeedItem] | str = Field(default_factory=list)
    feedItems: List[str] | str = Field(default_factory=list)
    transform_to_item: List[str] | str = Field(default_factory=list)
    pause_growth_items: List[str] = Field(default_factory=list)
    reset_growth_items: List[str] = Field(default_factory=list)
