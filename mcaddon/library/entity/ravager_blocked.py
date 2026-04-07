__all__ = ["EntityRavagerBlockedComponent", "BlockedReactionChoice"]

from typing import List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .event import EntityTriggerEvent
from .component import EntityComponent


class BlockedReactionChoice(BaseModel):
    weight: int
    value: Optional[EntityTriggerEvent] = None


@EntityComponent.register
class EntityRavagerBlockedComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ravager_blocked)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:ravager_blocked"

    knockback_strength: float = 3
    reaction_choices: List[BlockedReactionChoice] = Field(default_factory=list)
