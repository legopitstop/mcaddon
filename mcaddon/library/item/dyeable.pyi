from .component import ItemComponent

__all__ = ["ItemDyeableComponent"]

class ItemDyeableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_dyeable)
    """

    default_color: tuple[int, int, int] | str = ...
