__all__ = ["BlockMaterialInstancesComponent", "BlockMaterialInstance"]

from typing import Dict, Optional, ClassVar
from pydantic import Field, ConfigDict
from pydantic_core import core_schema
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import RenderMethod, TintMethod
from .component import BlockComponent


class BlockMaterialInstance(BaseModel):
    model_config = ConfigDict(extra="allow")

    texture: str
    alpha_masked_tint: Optional[bool] = None
    ambient_occlusion: Optional[bool] = None
    emissive: Optional[bool] = None
    face_dimming: Optional[bool] = None
    isotropic: bool = False
    render_method: RenderMethod = RenderMethod.OPAQUE
    tint_method: Optional[TintMethod | str | bool] = None

    @classmethod
    def __get_pydantic_core_schema__(cls, _source, handler):
        schema = handler(_source)
        return core_schema.no_info_wrap_validator_function(
            cls._wrap_parse,
            schema,
        )

    @classmethod
    def _wrap_parse(cls, v, handler):
        if isinstance(v, str):
            return handler({"texture": v})
        return handler(v)


@BlockComponent.register
class BlockMaterialInstancesComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_material_instances)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:material_instances"

    value: Dict[str, BlockMaterialInstance] = Field(default_factory=dict)

    def add(
        self, texture: BlockMaterialInstance, key: Optional[str] = None
    ) -> "BlockMaterialInstancesComponent":
        self.value[key or "*"] = texture
        return self

    @classmethod
    def __get_pydantic_core_schema__(cls, _source, handler):
        schema = handler(_source)
        return core_schema.no_info_wrap_validator_function(
            cls._wrap_parse,
            schema,
        )

    @classmethod
    def _wrap_parse(cls, v, handler):
        # If input already has a top-level 'value', don't wrap again.
        if isinstance(v, dict) and "value" in v:
            return handler(v)
        return handler({"value": v})
