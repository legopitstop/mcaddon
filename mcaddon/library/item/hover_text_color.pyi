from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemHoverTextColorComponent"]

class ItemHoverTextColorComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hover_text_color)
    """

    value: str
