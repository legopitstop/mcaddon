from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemUseAnimationComponent"]

class ItemUseAnimationComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_animation)
    """

    value: str
