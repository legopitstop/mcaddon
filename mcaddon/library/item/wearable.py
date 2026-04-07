__all__ = [
    "ItemWearableComponent",
]

from typing import Optional, ClassVar
from pydantic import Field
from mcaddon.library.constants import WearableSlot
from .component import ItemComponent


@ItemComponent.register
class ItemWearableComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_wearable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:wearable"

    protection: int = 0
    slot: WearableSlot
    hides_player_location: bool = False
    dispensable: Optional[bool] = Field(deprecated=True, default=None)
