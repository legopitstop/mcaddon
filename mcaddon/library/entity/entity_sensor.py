__all__ = ["EntityEntitySensorComponent", "Subsensor"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel, NumberRange
from mcaddon.library.filter import Filter
from .component import EntityComponent
from .event import EntityTriggerEvent


class Subsensor(BaseModel):
    cooldown: float = -1
    event: EntityTriggerEvent | str
    event_filters: Filter
    maximum_count: int = -1
    minimum_count: int = 1
    range: NumberRange = (10, 10)
    require_all: bool = False
    y_offset: float = 0


@EntityComponent.register
class EntityEntitySensorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_entity_sensor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:entity_sensor"

    find_players_only: bool = False
    relative_range: bool = True
    subsensors: List[Subsensor] = Field(default_factory=list)
