from .component import ItemComponent

__all__ = ["ItemStorageWeightLimitComponent"]

class ItemStorageWeightLimitComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_storage_weight_limit)
    """

    max_weight_limit: int = ...
