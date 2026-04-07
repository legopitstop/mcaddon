__all__ = ["EntityBlockSensorComponent", "BreakBlockSensor"]

from typing import List, ClassVar
from pydantic import Field

from mcaddon.library.filter import FilterTest
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class BreakBlockSensor(BaseModel):
    on_block_broken: str
    block_list: List[str] = Field(default_factory=list)


@EntityComponent.register
class EntityBlockSensorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_block_sensor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:block_sensor"

    on_break: List[BreakBlockSensor] = Field(default_factory=list)
    sensor_radius: float = 16
    sources: List[FilterTest] = Field(default_factory=list)
