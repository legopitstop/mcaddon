__all__ = ["EntityEnvironmentSensorComponent", "EnvironmentTrigger"]

from typing import List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.filter import Filter
from .component import EntityComponent


class EnvironmentTrigger(BaseModel):
    filters: Filter
    event: str


@EntityComponent.register
class EntityEnvironmentSensorComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_environment_sensor)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:environment_sensor"

    triggers: List[EnvironmentTrigger] | EnvironmentTrigger = Field(
        default_factory=list
    )
