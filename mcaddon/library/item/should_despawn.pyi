from .component import ItemComponent
from mcaddon import ValueComponent

__all__ = ["ItemShouldDespawnComponent"]

class ItemShouldDespawnComponent(ValueComponent, ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_should_despawn)
    """

    value: bool
