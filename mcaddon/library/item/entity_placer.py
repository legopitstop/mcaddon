__all__ = [
    "ItemEntityPlacerComponent",
]

from typing import List, ClassVar
from pydantic import Field

from mcaddon.core.base import BlockLike
from .component import ItemComponent


@ItemComponent.register
class ItemEntityPlacerComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_entity_placer)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:entity_placer"

    entity: str
    dispense_on: List[BlockLike] | BlockLike = Field(default_factory=list)
    use_on: List[BlockLike] | BlockLike = Field(default_factory=list)
