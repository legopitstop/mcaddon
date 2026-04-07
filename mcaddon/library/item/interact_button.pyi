from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemInteractButtonComponent"]

class ItemInteractButtonComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_interact_button)
    """

    value: str | bool
