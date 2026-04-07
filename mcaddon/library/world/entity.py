__all__ = ["EntityFormat", "LinksTag"]

from typing import List, Optional, Dict, Any
from pydantic import Field

from mcaddon.core.file import NbtFile
from mcaddon.core.types import Vector3, Vector2
from mcaddon.core.base import BaseModel


class LinksTag(BaseModel):
    entityID: int
    LinkID: int


class EntityFormat(NbtFile):
    Chested: bool
    Color: bool
    Color2: bool
    CustomName: Optional[str] = None
    CustomNameVisible: bool
    definitions: Optional[List[str]] = None
    FallDistance: float
    Fire: float
    identifier: str
    internalComponents: Dict[str, Any] = Field(default_factory=dict)
    Invulnerable: bool
    IsAngry: bool
    IsAutonomous: bool
    IsBaby: bool
    IsEating: bool
    IsGliding: bool
    IsGlobal: bool
    IsIllagerCaptain: bool
    IsOrphaned: bool
    IsOutOfControl: bool
    IsRoaring: bool
    IsScared: bool
    IsStunned: bool
    IsSwimming: bool
    IsTamed: bool
    IsTrusting: bool
    LastDimensionId: int
    LinksTag: LinksTag
    LootDropped: bool
    MarkVariant: int
    Motion: Vector3
    OnGround: bool
    OwnerNew: int = -1
    Persistent: bool
    PortalCooldown: int
    Pos: Vector3
    Rotation: Vector2
    Saddled: bool
    Sheared: bool
    ShowBottom: bool
    Sitting: bool
    SkinID: int
    Strength: int
    StrengthMax: int
    Tags: Optional[List[str]] = None
    UniqueID: int
    Variant: int
