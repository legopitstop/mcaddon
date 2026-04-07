__all__ = ["EntityLeashableComponent", "LeashablePreset"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.filter import Filter
from mcaddon.library.constants import LeashableSpringType
from .event import EntityTriggerEvent
from .component import EntityComponent


class LeashablePreset(BaseModel):
    filter: Optional[Filter] = None
    hard_distance: float = 7
    max_distance: float = 12
    rotation_adjustment: float = 0
    soft_distance: float = 4
    spring_type: LeashableSpringType = LeashableSpringType.DAMPENED


@EntityComponent.register
class EntityLeashableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_leashable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:leashable"

    can_be_cut: bool = True
    can_be_stolen: bool = False
    hard_distance: int = 6
    max_distance: int = 1
    on_leash: Optional[EntityTriggerEvent] = None
    on_unleash: Optional[EntityTriggerEvent] = None
    on_unleash_interact_only: bool = False
    presets: List[LeashablePreset] = Field(default_factory=list)
    soft_distance: int = 4
