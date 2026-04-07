from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemDisplayNameComponent"]

class ItemDisplayNameComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_display_name)
    """

    value: str
