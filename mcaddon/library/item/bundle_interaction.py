__all__ = [
    "ItemBundleInteractionComponent",
]

from typing import ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemBundleInteractionComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_bundle_interaction)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:bundle_interaction"

    num_viewable_slots: int = 12
