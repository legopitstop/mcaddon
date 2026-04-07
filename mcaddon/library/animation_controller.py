__all__ = ["AnimationControllers", "AnimationController", "AnimationState"]

from typing import Dict, List, Optional
from pydantic import Field
from molang.dsl import MolangExpr
import commentjson

from mcaddon.core.base import BaseModel
from mcaddon.core.file import ResourceFile
from mcaddon.library.pack import behaviorpack, resourcepack


class AnimationState(BaseModel):
    animations: List[str | Dict[str, MolangExpr]] = Field(default_factory=list)
    transitions: List[Dict[str, MolangExpr]] = Field(default_factory=list)
    particle_effects: List[Dict[str, str]] = Field(default_factory=list)
    sound_effects: List[Dict[str, str]] = Field(default_factory=list)
    blend_transition: Optional[float] = None
    blend_via_shortest_path: Optional[bool] = None


class AnimationController(BaseModel):
    initial_state: str = "default"
    states: Dict[str, AnimationState] = Field(default_factory=dict)


@behaviorpack("animation_controllers")
@resourcepack("animation_controllers")
class AnimationControllers(ResourceFile):
    TYPE_ID = "animation_controllers"
    format_version: str = "1.10.0"

    animation_controllers: Dict[str, AnimationController] = Field(default_factory=dict)

    def get(self, identifier: str) -> Optional[AnimationController]:
        return self.animation_controllers.get(identifier)

    @classmethod
    def loads(cls, obj: str) -> "AnimationControllers":
        data = commentjson.loads(obj)
        result = AnimationControllers()
        for k, v in data["animation_controllers"].items():
            result.animation_controllers[k] = AnimationController.model_validate(v)
        return result
