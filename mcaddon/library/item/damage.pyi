from .component import ItemComponent
from mcaddon.core.base import ValueComponent

__all__ = ["ItemDamageComponent"]

class ItemDamageComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_damage)
    """

    value: int
