from .component import BlockComponent
from .geometry import BlockGeometryComponent
from .material_instances import BlockMaterialInstancesComponent
from mcaddon.core.base import ValueComponent

__all__ = ["BlockEmbeddedVisualComponent"]

class BlockEmbeddedVisualComponent(ValueComponent, BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_embedded_visual)
    """

    geometry: BlockGeometryComponent | None
    material_instances: BlockMaterialInstancesComponent | None
