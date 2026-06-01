__all__ = [
    "TemplatePool",
    "TemplatePoolElement",
    "SinglePoolElement",
    "ElementInstance",
    "TemplatePool",
]

from typing import List
from pydantic import Field

from mcaddon.core.file import ResourceFile
from mcaddon.core.base import BaseModel, BaseTypedModel, TypedModel
from mcaddon.library.common import BaseDescription
from mcaddon.library.pack import behaviorpack


class TemplatePoolElement(BaseTypedModel):
    pass


@TemplatePoolElement.register
class SinglePoolElement(TypedModel):
    TYPE_ID = "single_pool_element"
    element_type: str = TYPE_ID

    location: str
    processors: str


class ElementInstance(BaseModel):
    element: TemplatePoolElement
    weight: int


@behaviorpack("worldgen/loot_tables")
class TemplatePool(ResourceFile):
    TYPE_ID = "minecraft:template_pool"

    description: BaseDescription = BaseDescription(identifier="minecraft:template_pool")
    elements: List[ElementInstance] = Field(default_factory=list)

    @property
    def id(self) -> str:
        return self.description.identifier
