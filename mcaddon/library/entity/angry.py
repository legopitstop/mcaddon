__all__ = ["EntityAngryComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field

from mcaddon.library.filter import Filter
from mcaddon.core.base import NumberRange
from .component import EntityComponent
from .event import EntityTriggerEvent


@EntityComponent.register
class EntityAngryComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_angry)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:angry"

    angry_sound: Optional[str] = None
    broadcast_anger: bool = False
    broadcastAnger: bool = False
    broadcast_anger_on_attack: bool = False
    broadcast_anger_on_being_attacked: bool = False
    broadcast_anger_when_dying: bool = False
    broadcast_filters: Optional[Filter] = None
    broadcast_range: int = 20
    broadcastRange: int = 20
    broadcast_targets: List[str] = Field(default_factory=list)
    calm_event: Optional[EntityTriggerEvent] = None
    duration: int = 25
    duration_delta: int = 0
    filters: Optional[Filter] = None
    sound_interval: Optional[NumberRange] = None
