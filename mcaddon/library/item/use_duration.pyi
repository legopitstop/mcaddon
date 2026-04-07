from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemUseDurationComponent"]

class ItemUseDurationComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_duration)
    """

    value: float
