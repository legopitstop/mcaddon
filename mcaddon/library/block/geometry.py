__all__ = [
    "BlockGeometryComponent",
]

from molang.dsl import MolangExpr
from typing import Dict, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import ValueComponent
from .component import BlockComponent


@BlockComponent.register
class BlockGeometryComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_geometry)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:geometry"

    identifier: str = "minecraft:geometry.full_block"
    bone_visibility: Dict[str, bool | MolangExpr] = Field(default_factory=dict)
    culling: Optional[str] = None
    culling_layer: Optional[str] = None
    uv_lock: Optional[bool] = None

    @classmethod
    def _wrap_parse(cls, v, handler):
        if not isinstance(v, dict):
            v = {"identifier": v}
        return handler(v)
