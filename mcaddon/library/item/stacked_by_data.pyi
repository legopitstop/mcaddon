from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemStackedByDataComponent"]

class ItemStackedByDataComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_stacked_by_data)
    """

    value: bool
