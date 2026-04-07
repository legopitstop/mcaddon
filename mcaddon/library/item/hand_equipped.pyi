from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemHandEquippedComponent"]

class ItemHandEquippedComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hand_equipped)
    """

    value: bool = ...
