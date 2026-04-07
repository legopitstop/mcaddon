__all__ = ["Animations", "Animation", "BoneAnimation", "AnimationEffect"]

from typing import Dict, Optional, Tuple, List
import commentjson
from molang.dsl import MolangExpr
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.core.file import ResourceFile
from mcaddon.core.types import Number
from mcaddon.library.constants import LerpMode, LoopMode
from mcaddon.library.pack import behaviorpack, resourcepack

AnimateVec3 = Tuple[Number | MolangExpr, Number | MolangExpr, Number | MolangExpr]


class AnimValue3(BaseModel):
    post: AnimateVec3
    pre: Optional[AnimateVec3] = None
    lerp_mode: Optional[LerpMode] = None


class AnimValue2(BaseModel):
    x: Optional[MolangExpr] = None
    y: Optional[MolangExpr] = None
    z: Optional[MolangExpr] = None


AnimValue = AnimateVec3 | Dict[str, AnimateVec3 | AnimValue3] | List[AnimValue2]


class BoneAnimation(BaseModel):
    rotation: Optional[AnimValue] = None
    position: Optional[AnimValue] = None
    scale: Optional[Number | MolangExpr | AnimValue] = None
    relative_to: Dict[str, str] = Field(default_factory=dict)


class AnimationEffect(BaseModel):
    effect: str
    pre_effect_script: Optional[MolangExpr] = None


class Animation(BaseModel):
    loop: Optional[bool | LoopMode] = None
    override_previous_animation: Optional[bool] = None
    animation_length: Optional[Number] = None
    anim_time_update: Optional[MolangExpr] = None
    start_delay: Optional[MolangExpr | Number] = None
    bones: Dict[str, BoneAnimation] = Field(default_factory=dict)
    sound_effects: Dict[str, AnimationEffect] = Field(default_factory=dict)
    particle_effects: Dict[str, AnimationEffect] = Field(default_factory=dict)


@behaviorpack("animations")
@resourcepack("animations")
class Animations(ResourceFile):
    TYPE_ID = "animations"
    format_version: str = "1.10.0"

    animations: Dict[str, Animation] = Field(default_factory=dict)

    def get(self, identifier: str) -> Optional[Animation]:
        return self.animations.get(identifier)

    @classmethod
    def loads(cls, obj: str) -> "Animations":
        data = commentjson.loads(obj)
        result = Animations()
        for k, v in data["animations"].items():
            result.animations[k] = Animation.model_validate(v)
        return result
