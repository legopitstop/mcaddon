__all__ = ["Attachable", "AttachableDescription", "AttachableScripts"]

from typing import Dict, List, Optional
from pydantic import Field

from mcaddon.library.pack import resourcepack
from mcaddon.core.file import ResourceFile
from mcaddon.core.base import BaseModel
from mcaddon.library.common import BaseDescription


class AttachableScripts(BaseModel):
    parent_setup: Optional[str] = None
    initialize: Optional[List[str]] = Field(default_factory=list)
    pre_animation: Optional[List[str]] = Field(default_factory=list)
    animate: Optional[List[str | Dict[str, str]]] = Field(default_factory=list)


class AttachableDescription(BaseDescription):
    materials: Dict[str, str] = Field(default_factory=dict)
    textures: Dict[str, str] = Field(default_factory=dict)
    geometry: Dict[str, str] = Field(default_factory=dict)
    animations: Dict[str, str] = Field(default_factory=dict)
    item: Dict[str, str] = Field(default_factory=dict)
    render_controllers: List[str] = Field(default_factory=list)
    scripts: Optional[AttachableScripts] = None


@resourcepack("attachables")
class Attachable(ResourceFile):
    TYPE_ID = "minecraft:attachable"
    format_version: str = "1.10.0"

    description: AttachableDescription

    @property
    def id(self) -> str:
        return self.description.identifier
