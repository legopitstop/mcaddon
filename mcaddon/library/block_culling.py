__all__ = ["BlockCulling", "CullingRule", "GeometryPart"]

from typing import List, Optional
from pydantic import Field

from mcaddon.core.file import ResourceFile
from mcaddon.core.base import BaseModel
from .pack import resourcepack
from .common import BaseDescription
from .constants import Direction, BlockFace


class GeometryPart(BaseModel):
    bone: str
    cube: Optional[int] = None
    face: Optional[BlockFace] = None


class CullingRule(BaseModel):
    direction: Direction
    geometry_part: GeometryPart


@resourcepack("block_culling")
class BlockCulling(ResourceFile):
    TYPE_ID = "minecraft:block_culling_rules"

    description: BaseDescription = BaseDescription(identifier="minecraft:test")
    rules: List[CullingRule] = Field(default_factory=list)
