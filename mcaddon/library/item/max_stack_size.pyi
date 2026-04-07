from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemMaxStackSizeComponent"]

class ItemMaxStackSizeComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_max_stack_size)
    """

    value: int = ...
