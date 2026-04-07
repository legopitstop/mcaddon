__all__ = [
    "StructureFormat",
    "StructureFile",
    "Palette",
    "BlockPalette",
    "BlockPositionData",
]

from typing import List, ClassVar, Dict, Any
from pydantic import Field
from mcaddon.core.file import NbtFile
from mcaddon.core.types import Vector3
from mcaddon.core.base import BaseModel
from .world import EntityFormat, BlockEntityFormat


class BlockPalette(BaseModel):
    name: str
    version: int
    states: Dict[str, Any] = Field(default_factory=dict)


class BlockPositionData(BaseModel):
    block_entity_data: BlockEntityFormat


class Palette(BaseModel):
    block_palette: List[BlockPalette] = Field(default_factory=list)
    block_position_data: Dict[str, BlockPositionData] = Field(default_factory=dict)


class StructureFormat(BaseModel):
    block_indices: List[List[int]] = Field(default_factory=list)
    entities: List[EntityFormat] = Field(default_factory=list)
    palette: Dict[str, Palette] = Field(default_factory=dict)


# @behavior("structures")
class StructureFile(NbtFile):
    extension: ClassVar[str] = ".mcstructure"

    format_version: int = 1
    size: Vector3
    structure: StructureFormat
    structure_world_origin: Vector3
