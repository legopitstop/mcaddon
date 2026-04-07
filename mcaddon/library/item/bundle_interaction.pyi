from .component import ItemComponent

__all__ = ["ItemBundleInteractionComponent"]

class ItemBundleInteractionComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_bundle_interaction)
    """

    num_viewable_slots: int = ...
