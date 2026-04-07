from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemCanDestroyInCreativeComponent"]

class ItemCanDestroyInCreativeComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_can_destroy_in_creative)
    """

    value: bool
