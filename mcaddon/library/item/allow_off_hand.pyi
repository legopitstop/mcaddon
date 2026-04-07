from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemAllowOffHandComponent"]

class ItemAllowOffHandComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_allow_off_hand)
    """

    value: bool
