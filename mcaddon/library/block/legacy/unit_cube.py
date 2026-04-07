__all__ = [
    "BlockUnitCubeComponent",
]

from ..component import BlockComponent
from typing import ClassVar
from deprecated import deprecated


@deprecated(
    "This component is deprecated, use BlockGeometryComponent.identifier = 'minecraft:geometry.full_block' instead."
)
@BlockComponent.register
class BlockUnitCubeComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_unit_cube)

    This type is now deprecated, and no longer in use in the latest versions of Minecraft.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:unit_cube"
