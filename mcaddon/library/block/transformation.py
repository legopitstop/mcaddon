__all__ = [
    "BlockTransformationComponent",
]

from typing import Optional, ClassVar
from mcaddon.core.types import Vector3
from .component import BlockComponent


@BlockComponent.register
class BlockTransformationComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_transformation)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:transformation"

    rotation: Optional[Vector3] = None
    rotation_pivot: Optional[Vector3] = None
    scale: Optional[Vector3] = None
    scale_pivot: Optional[Vector3] = None
    translation: Optional[Vector3] = None

    def rotate(self, rotation: Vector3) -> "BlockTransformationComponent":
        self.rotation = rotation
        return self

    def inflate(self, scale: Vector3) -> "BlockTransformationComponent":
        self.scale = scale
        return self

    def move(self, translation: Vector3) -> "BlockTransformationComponent":
        self.translation = translation
        return self
