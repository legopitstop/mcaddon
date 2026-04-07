from .component import ItemComponent
from mcaddon.library.constants import WearableSlot

__all__ = ["ItemWearableComponent"]

class ItemWearableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_wearable)
    """

    protection: int
    slot: WearableSlot
    hides_player_location: bool = ...
    dispensable: bool | None = ...
