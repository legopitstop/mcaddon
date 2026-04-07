__all__ = [
    "BlockItemVisualComponent",
]

from typing import Optional, ClassVar
from .material_instances import BlockMaterialInstancesComponent
from .geometry import BlockGeometryComponent
from .component import BlockComponent


@BlockComponent.register
class BlockItemVisualComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_item_visual)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:item_visual"

    geometry: Optional[BlockGeometryComponent] = None
    material_instances: Optional[BlockMaterialInstancesComponent] = None
