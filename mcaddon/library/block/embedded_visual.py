__all__ = [
    "BlockEmbeddedVisualComponent",
]

from typing import Optional, ClassVar

from mcaddon.core.base import ValueComponent
from .component import BlockComponent
from .geometry import BlockGeometryComponent
from .material_instances import BlockMaterialInstancesComponent


@BlockComponent.register
class BlockEmbeddedVisualComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_embedded_visual)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:embedded_visual"

    geometry: Optional[BlockGeometryComponent] = None
    material_instances: Optional[BlockMaterialInstancesComponent] = None
