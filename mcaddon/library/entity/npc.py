__all__ = ["EntityNPCComponent", "NPCOffsets", "NPCData", "NPCSkin"]

from typing import Optional, List, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.core.types import Vector3
from .component import EntityComponent


class NPCOffsets(BaseModel):
    translate: Optional[Vector3] = None
    scale: Optional[Vector3] = None


class NPCSkin(BaseModel):
    variant: Optional[int] = None


class NPCData(BaseModel):
    portrait_offsets: Optional[NPCOffsets] = None
    picker_offsets: Optional[NPCOffsets] = None
    skin_list: List[NPCSkin] = Field(default_factory=list)


@EntityComponent.register
class EntityNPCComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_npc)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:npc"

    npc_data: NPCData
