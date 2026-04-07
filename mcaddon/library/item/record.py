__all__ = [
    "ItemRecordComponent",
]

from typing import ClassVar
from .component import ItemComponent


@ItemComponent.register
class ItemRecordComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_record)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:record"

    sound_event: str
    comparator_signal: int = 1
    duration: float = 0
