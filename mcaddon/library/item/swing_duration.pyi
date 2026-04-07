from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemSwingDurationComponent"]

class ItemSwingDurationComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_swing_duration)
    """

    value: float = ...
