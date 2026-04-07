__all__ = [
    "LegacyBlockBoneVisibilityComponent",
]

from molang.dsl import MolangExpr
from mcaddon.core.base import ValueComponent
from typing import Dict
from ..component import BlockComponent
from deprecated import deprecated

@deprecated(
    "This component is deprecated, use BlockGeometryComponent.bone_visibility instead."
)
@BlockComponent.register
class LegacyBlockBoneVisibilityComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_bone_visibility)

    Use minecraft:geometry.bone_visibility in newer format versions.
    """

    value: Dict[str, MolangExpr] = ...
