__all__ = ["EntityNameableComponent"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from .event import EntityTriggerEvent
from .component import EntityComponent


class NameAction(BaseModel):
    name_filter: Optional[str] = None
    on_named: Optional[EntityTriggerEvent] = None


@EntityComponent.register
class EntityNameableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_nameable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:nameable"

    allow_name_tag_renaming: bool = True
    always_show: bool = False
    default_trigger: Optional[EntityTriggerEvent] = None
    name_actions: List[NameAction] = Field(default_factory=list)
