__all__ = ["CraftingItemsCatalog", "GroupIdentifier", "CatalogGroup", "CatalogCategory"]

from typing import Optional, List
from pydantic import Field, field_validator

from mcaddon.core.base import BaseModel
from mcaddon.core.file import ResourceFile
from .pack import behaviorpack
from .constants import CreativeCategory


class GroupIdentifier(BaseModel):
    name: str
    icon: Optional[str]


class CatalogGroup(BaseModel):
    group_identifier: Optional[GroupIdentifier] = None
    items: List[str] = Field(default_factory=list)


class CatalogCategory(BaseModel):
    category_name: CreativeCategory
    groups: List[CatalogGroup] = Field(default_factory=list)

    @field_validator("category_name", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return CreativeCategory.parse(v)


@behaviorpack("item_catalog")
class CraftingItemsCatalog(ResourceFile):
    TYPE_ID = "minecraft:crafting_items_catalog"
    format_version: str = "1.21.60"

    categories: List[CatalogCategory] = Field(default_factory=list)
