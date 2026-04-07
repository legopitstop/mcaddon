from .component import ItemComponent

__all__ = ["ItemFuelComponent"]

class ItemFuelComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fuel)
    """

    duration: int
