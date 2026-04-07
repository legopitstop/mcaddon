from .component import BlockComponent
from .geometry import BlockGeometryComponent
from .material_instances import BlockMaterialInstancesComponent

__all__ = ["BlockItemVisualComponent"]

class BlockItemVisualComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_item_visual)
    """

    geometry: BlockGeometryComponent | None
    material_instances: BlockMaterialInstancesComponent | None
