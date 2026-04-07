__all__ = ["EntityAmbientSoundIntervalComponent"]

from typing import List, Optional, ClassVar
from molang.dsl import MolangExpr
from pydantic import Field
from mcaddon.core.base import BaseModel
from .component import EntityComponent


class EventName(BaseModel):
    condition: MolangExpr
    event_name: str


@EntityComponent.register
class EntityAmbientSoundIntervalComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ambient_sound_interval)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:ambient_sound_interval"

    event_name: Optional[str] = None
    event_names: List[EventName] = Field(default_factory=list)
    range: float = 16
    value: float = 0
