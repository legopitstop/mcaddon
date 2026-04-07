__all__ = ["Entity", "EntityDescription", "EntityScripts", "EntityProperty"]

from typing import Dict, List, Optional
from pydantic import Field, field_validator

from mcaddon.core.file import ResourceFile
from mcaddon.core.base import Number, BaseModel, ComponentSet
from mcaddon.library.common import BaseDescription
from mcaddon.library.pack import behaviorpack
from mcaddon.library.constants import EntityPropertyType
from .component import EntityComponent
from .event import EntityEvent


class EntityProperty(BaseModel):
    type: EntityPropertyType
    values: List[str] = Field(default_factory=list)
    range: List[Number] = Field(default_factory=list, max_length=2)
    default: str | bool | Number
    client_sync: bool = False

    @field_validator("type", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return EntityPropertyType.parse(v)


class EntityScripts(BaseModel):
    animate: List[str | Dict[str, str]] = Field(default_factory=list)


class EntityDescription(BaseDescription):
    spawn_category: Optional[str] = None
    properties: Dict[str, EntityProperty] = Field(default_factory=dict)
    animations: Dict[str, str] = Field(default_factory=dict)
    scripts: Optional[EntityScripts] = None
    runtime_identifier: Optional[str] = None
    is_spawnable: Optional[bool] = None
    is_summonable: Optional[bool] = None
    is_experimental: Optional[bool] = None


@behaviorpack("entities")
class Entity(ResourceFile):
    """
    Defines an entity.
    """

    TYPE_ID = "minecraft:entity"
    format_version: str = "1.21.50"

    description: EntityDescription = EntityDescription(identifier="minecraft:creeper")
    components: ComponentSet[EntityComponent] = Field(default_factory=ComponentSet)
    component_groups: Dict[str, ComponentSet[EntityComponent]] = Field(
        default_factory=dict
    )

    events: Optional[Dict[str, EntityEvent]] = None

    @property
    def id(self) -> str:
        return self.description.identifier
