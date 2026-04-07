from .component import ItemComponent

__all__ = ["ItemStorageWeightModifierComponent"]

class ItemStorageWeightModifierComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_storage_weight_modifier)
    """

    weight_in_storage_item: int = ...
