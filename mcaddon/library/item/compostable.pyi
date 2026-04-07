from .component import ItemComponent

__all__ = ["ItemCompostableComponent"]

class ItemCompostableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_compostable)
    """

    composting_chance: int
