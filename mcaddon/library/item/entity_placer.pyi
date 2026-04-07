from .component import ItemComponent
from mcaddon.core.base import BlockLike

__all__ = ["ItemEntityPlacerComponent"]

class ItemEntityPlacerComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_entity_placer)
    """

    entity: str
    dispense_on: list[BlockLike] | BlockLike = ...
    use_on: list[BlockLike] | BlockLike = ...
