from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemGlintComponent"]

class ItemGlintComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_glint)
    """

    value: bool
