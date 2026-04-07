__all__ = [
    "RenderControllers",
    "RenderController",
    "MolangColor",
    "RenderControllerArrays",
    "RenderControllerUVAnim",
]

from typing import Dict, Optional, List, Tuple
from molang.dsl import MolangExpr, texture, geometry, material
from pydantic import Field
from mcaddon.core.types import Number
from mcaddon.core.base import BaseModel, MolangColor
from mcaddon.core.file import ResourceFile
from mcaddon.library.pack import resourcepack
import commentjson


class RenderControllerArrays(BaseModel):
    textures: Dict[str, List[MolangExpr]] = Field(default_factory=dict)
    geometries: Dict[str, List[MolangExpr]] = Field(default_factory=dict)
    materials: Dict[str, List[MolangExpr]] = Field(default_factory=dict)


class RenderControllerUVAnim(BaseModel):
    offset: Tuple[Number | MolangExpr, Number | MolangExpr] = (0, 0)
    scale: Tuple[Number | MolangExpr, Number | MolangExpr] = (1.0, 1.0)


class RenderController(BaseModel):
    geometry: MolangExpr = geometry.default
    materials: List[Dict[str, MolangExpr]] = Field(default=[{"*": material.default}])
    textures: List[MolangExpr] = Field(default=[texture.default])

    arrays: Optional[RenderControllerArrays] = None
    ignore_lighting: Optional[bool] = None
    filter_lighting: Optional[bool] = None
    rebuild_animation_matrices: Optional[bool] = None
    overlay_color: Optional[MolangColor] = None
    is_hurt_color: Optional[MolangColor] = None
    on_fire_color: Optional[MolangColor] = None
    color: Optional[MolangColor] = None
    light_color_multiplier: Optional[Number] = None
    uv_anim: Optional[RenderControllerUVAnim] = None
    part_visibility: List[Dict[str, bool | MolangExpr]] = Field(default_factory=list)


@resourcepack("render_controllers")
class RenderControllers(ResourceFile):
    TYPE_ID = "render_controllers"
    format_version: str = "1.10.0"

    render_controllers: Dict[str, RenderController] = Field(default_factory=dict)

    def get(self, identiifer: str) -> Optional[RenderController]:
        return self.render_controllers.get(identiifer)

    @classmethod
    def loads(cls, obj: str) -> "RenderControllers":
        data = commentjson.loads(obj)
        result = RenderControllers()
        for k, v in data["render_controllers"].items():
            result.render_controllers[k] = RenderController.model_validate(v)
        return result
