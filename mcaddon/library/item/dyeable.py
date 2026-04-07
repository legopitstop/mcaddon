__all__ = [
    "ItemDyeableComponent",
]

from typing import ClassVar
from typing import Tuple
from .component import ItemComponent


@ItemComponent.register
class ItemDyeableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_dyeable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:dyeable"

    default_color: Tuple[int, int, int] | str = (255, 255, 255)
