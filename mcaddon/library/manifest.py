__all__ = ["Manifest", "Header", "Module", "Metadata", "Dependency"]

from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID
from mcaddon.core.file import JsonFile
from mcaddon.core.base import BaseModel
from .constants import Capability, ProductType, ModuleType, PackScope
from pathlib import Path
import commentjson


class Header(BaseModel):
    uuid: UUID
    name: Optional[str] = "pack.name"
    description: Optional[str] = "pack.description"
    version: List[int] = Field(default=[1, 0, 0])
    min_engine_version: List[int] = Field(default=[1, 21, 80])
    pack_scope: Optional[PackScope] = None


class Module(BaseModel):
    type: ModuleType
    uuid: UUID
    version: List[int] = Field(default=[1, 0, 0])
    description: Optional[str] = None
    language: Optional[str] = None
    entry: Optional[str] = None


class Metadata(BaseModel):
    license: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    generated_with: Dict[str, str] = Field(default_factory=dict)
    product_type: Optional[ProductType] = None
    url: Optional[str] = None


class Dependency(BaseModel):
    version: str | List[int] = Field(default=[1, 0, 0])
    uuid: Optional[UUID] = None
    module_name: Optional[str] = None


class Manifest(JsonFile):
    format_version: int = 2
    header: Header
    modules: List[Module] = Field(default_factory=list)
    dependencies: List[Dependency] = Field(default_factory=list)
    capabilities: List[Capability] = Field(default_factory=list)
    metadata: Optional[Metadata] = None

    def get_pack_type(self) -> str | None:
        for mod in self.modules:
            type = mod.type.get_pack_type()
            if type is not None:
                return type
        return None

    @staticmethod
    def guess_pack_type(filename: str | Path) -> Optional[str]:
        with open(filename, "r") as fd:
            data = commentjson.load(fd)
            if "modules" not in data:
                return None

            for mod in data["modules"]:
                if "type" in mod:
                    match mod["type"]:
                        case "data":
                            return "behavior_pack"
                        case "resources":
                            return "resource_pack"
                        case "skin_pack":
                            return "skin_pack"
        return None
