__all__ = ["EntityTrustingComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from .event import EntityTriggerEvent
from .component import EntityComponent


@EntityComponent.register
class EntityTrustingComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trusting)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:trusting"

    probability: float = 1
    trust_event: Optional[EntityTriggerEvent] = None
    trust_items: List[str] = Field(default_factory=list)
