from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemLiquidClippedComponent"]

class ItemLiquidClippedComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_liquid_clipped)
    """

    value: bool
