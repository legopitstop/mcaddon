__all__ = ["EntityPlayComponent", "PlayFriendType"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.types import Vector3
from mcaddon.library.filter import Filter
from mcaddon.core.base import BaseModel
from mcaddon.library.entity.component import EntityComponent, EntityBehaviorComponent


class PlayFriendType(BaseModel):
    filters: Filter


@EntityComponent.register
class EntityPlayComponent(EntityBehaviorComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_play)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:behavior.play"

    chance_to_start: float = 0
    follow_distance: int = 2
    friend_search_area: Vector3 = (6, 3, 6)
    friend_types: Optional[List[PlayFriendType] | PlayFriendType] = Field(
        default_factory=list
    )
    max_play_duration_seconds: float = 50
    random_pos_search_height: int = 3
    random_pos_search_range: int = 16
    speed_multiplier: float = 1
