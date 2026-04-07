from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemFireResistantComponent"]

class ItemFireResistantComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fire_resistant)
    """

    value: bool = ...
