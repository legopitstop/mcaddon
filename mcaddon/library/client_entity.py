__all__ = ["ClientEntity", "ClientEntityDescription"]

from typing import Dict, List, Optional
from pydantic import Field, field_validator
from molang.dsl import MolangExpr

from mcaddon.core.file import ResourceFile
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import ClientEntityVariable
from .common import BaseDescription
from .pack import resourcepack


class SpawnEgg(BaseModel):
    texture: Optional[str] = None
    base_color: Optional[str] = None
    overlay_color: Optional[str] = None
    texture_index: Optional[int] = None


class ClientEntityScripts(BaseModel):
    pre_animation: List[str] = Field(default_factory=list)
    animate: List[str | Dict[str, str]] = Field(default_factory=list)
    initialize: List[str] = Field(default_factory=list)
    variables: Dict[str, ClientEntityVariable] = Field(default_factory=dict)

    @field_validator("variables", mode="before")
    @classmethod
    def coerce_enum(cls, v):
        return {k: ClientEntityVariable.parse(v) for k, v in v.items()}

    # 1.10
    should_update_effects_offscreen: Optional[MolangExpr] = None
    should_update_bones_and_effects_offscreen: Optional[MolangExpr] = None
    scale: Optional[MolangExpr] = None
    scaleX: Optional[MolangExpr] = None
    scaleY: Optional[MolangExpr] = None
    scaleZ: Optional[MolangExpr] = None
    scalex: Optional[MolangExpr] = None
    scaley: Optional[MolangExpr] = None
    scalez: Optional[MolangExpr] = None


class ClientEntityDescription(BaseDescription):
    min_engine_version: Optional[str] = None
    materials: Dict[str, str] = Field(default_factory=dict)
    textures: Dict[str, str] = Field(default_factory=dict)
    geometry: Dict[str, str] = Field(default_factory=dict)
    animations: Dict[str, str] = Field(default_factory=dict)
    particle_effects: Dict[str, str] = Field(default_factory=dict)
    sound_effects: Dict[str, str] = Field(default_factory=dict)
    play_sound: Dict[str, str] = Field(default_factory=dict)
    render_controllers: List[str | Dict[str, str]] = Field(default_factory=list)
    scripts: Optional[ClientEntityScripts] = None
    spawn_egg: Optional[SpawnEgg] = None
    enable_attachables: bool = False

    # 1.10
    animation_controllers: List[Dict[str, str]] = Field(default_factory=list)
    particle_emitters: Dict[str, str] = Field(default_factory=dict)
    held_item_ignores_lighting: Optional[bool] = None
    hide_armor: Optional[bool] = None


@resourcepack("entities")
class ClientEntity(ResourceFile):
    TYPE_ID = "minecraft:client_entity"
    format_version: str = "1.10.0"

    description: ClientEntityDescription

    @property
    def id(self) -> str:
        return self.description.identifier
