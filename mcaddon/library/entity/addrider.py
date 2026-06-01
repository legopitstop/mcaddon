__all__ = ["EntityAddriderComponent", "Rider"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel

from .component import EntityComponent


class Rider(BaseModel):
    entity_type: str
    spawn_event: Optional[str] = None


@EntityComponent.register
class EntityAddriderComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_addrider)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:addrider"

    entity_type: Optional[str] = None
    spawn_event: Optional[str] = None

    riders: List[Rider] = Field(default_factory=list)
